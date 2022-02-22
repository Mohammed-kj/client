import hashlib
import io
import logging
import os
from typing import Any, cast, Dict, List, Optional, Sequence, Type, TYPE_CHECKING, Union

import wandb
from wandb.sdk.interface import _dtypes
from wandb.util import (
    ensure_matplotlib_figure,
    generate_id,
    get_full_typename,
    get_module,
    is_matplotlib_typename,
    is_pytorch_tensor_typename,
    to_forward_slash_path,
)

from ._batched_media import BatchableMedia
from ._bounding_boxes2d import BoundingBoxes2D
from ._classes import Classes
from ._image_mask import ImageMask

if TYPE_CHECKING:
    import matplotlib  # type: ignore
    import numpy as np  # type: ignore
    import torch  # type: ignore
    import PIL  # type: ignore

    from _media import Media
    from wandb.apis.public import Artifact as PublicArtifact
    from wandb.sdk.wandb_artifacts import Artifact
    from wandb.sdk.wandb_run import Run

    ImageDataType = Union[
        "matplotlib.artist.Artist", "PIL.Image", "TorchTensorType", "np.ndarray"
    ]
    ImageDataOrPathType = Union[str, "Image", ImageDataType]
    TorchTensorType = Union["torch.Tensor", "torch.Variable"]


class Image(BatchableMedia):
    """Format images for logging to W&B.

    Arguments:
        data_or_path: (numpy array, string, io) Accepts numpy array of
            image data, or a PIL image. The class attempts to infer
            the data format and converts it.
        mode: (string) The PIL mode for an image. Most common are "L", "RGB",
            "RGBA". Full explanation at https://pillow.readthedocs.io/en/4.2.x/handbook/concepts.html#concept-modes.
        caption: (string) Label for display of image.

    Examples:
        ### Create a wandb.Image from a numpy array
        <!--yeadoc-test:log-image-numpy->
        ```python
        import numpy as np
        import wandb

        wandb.init()
        examples = []
        for i in range(3):
            pixels = np.random.randint(low=0, high=256, size=(100, 100, 3))
            image = wandb.Image(pixels, caption=f"random field {i}")
            examples.append(image)
        wandb.log({"examples": examples})
        ```

        ### Create a wandb.Image from a PILImage
        <!--yeadoc-test:log-image-pil->
        ```python
        import numpy as np
        from PIL import Image as PILImage
        import wandb

        wandb.init()
        examples = []
        for i in range(3):
            pixels = np.random.randint(low=0, high=256, size=(100, 100, 3), dtype=np.uint8)
            pil_image = PILImage.fromarray(pixels, mode="RGB")
            image = wandb.Image(pil_image, caption=f"random field {i}")
            examples.append(image)
        wandb.log({"examples": examples})
        ```
    """

    MAX_ITEMS = 108

    # PIL limit
    MAX_DIMENSION = 65500

    _log_type = "image-file"

    format: Optional[str]
    _grouping: Optional[str]
    _caption: Optional[str]
    _width: Optional[int]
    _height: Optional[int]
    _image: Optional["PIL.Image"]
    _classes: Optional["Classes"]
    _boxes: Optional[Dict[str, "BoundingBoxes2D"]]
    _masks: Optional[Dict[str, "ImageMask"]]

    def __init__(
        self,
        data_or_path: "ImageDataOrPathType",
        mode: Optional[str] = None,
        caption: Optional[str] = None,
        grouping: Optional[str] = None,
        classes: Optional[Union["Classes", Sequence[dict]]] = None,
        boxes: Optional[Union[Dict[str, "BoundingBoxes2D"], Dict[str, dict]]] = None,
        masks: Optional[Union[Dict[str, "ImageMask"], Dict[str, dict]]] = None,
    ) -> None:
        super().__init__()
        # TODO: We should remove grouping, it's a terrible name and I don't
        # think anyone uses it.

        self._grouping = None
        self._caption = None
        self._width = None
        self._height = None
        self._image = None
        self._classes = None
        self._boxes = None
        self._masks = None

        # Allows the user to pass an Image object as the first parameter and have a perfect copy,
        # only overriding additional metdata passed in. If this pattern is compelling, we can generalize.
        if isinstance(data_or_path, Image):
            self._initialize_from_wbimage(data_or_path)
        elif isinstance(data_or_path, str):
            self._initialize_from_path(data_or_path)
        else:
            self._initialize_from_data(data_or_path, mode)

        self._set_initialization_meta(grouping, caption, classes, boxes, masks)

    def _set_initialization_meta(
        self,
        grouping: Optional[str] = None,
        caption: Optional[str] = None,
        classes: Optional[Union["Classes", Sequence[dict]]] = None,
        boxes: Optional[Union[Dict[str, "BoundingBoxes2D"], Dict[str, dict]]] = None,
        masks: Optional[Union[Dict[str, "ImageMask"], Dict[str, dict]]] = None,
    ) -> None:
        if grouping is not None:
            self._grouping = grouping

        if caption is not None:
            self._caption = caption

        total_classes = {}

        if boxes:
            if not isinstance(boxes, dict):
                raise ValueError('Images "boxes" argument must be a dictionary')
            boxes_final: Dict[str, BoundingBoxes2D] = {}
            for key in boxes:
                box_item = boxes[key]
                if isinstance(box_item, BoundingBoxes2D):
                    boxes_final[key] = box_item
                elif isinstance(box_item, dict):
                    # TODO: Consider injecting top-level classes if user-provided is empty
                    boxes_final[key] = BoundingBoxes2D(box_item, key)
                total_classes.update(boxes_final[key]._class_labels)
            self._boxes = boxes_final

        if masks:
            if not isinstance(masks, dict):
                raise ValueError('Images "masks" argument must be a dictionary')
            masks_final: Dict[str, ImageMask] = {}
            for key in masks:
                mask_item = masks[key]
                if isinstance(mask_item, ImageMask):
                    masks_final[key] = mask_item
                elif isinstance(mask_item, dict):
                    # TODO: Consider injecting top-level classes if user-provided is empty
                    masks_final[key] = ImageMask(mask_item, key)
                if hasattr(masks_final[key], "_val"):
                    total_classes.update(masks_final[key]._val["class_labels"])
            self._masks = masks_final

        if classes is not None:
            if isinstance(classes, Classes):
                total_classes.update(
                    {val["id"]: val["name"] for val in classes._class_set}
                )
            else:
                total_classes.update({val["id"]: val["name"] for val in classes})

        if len(total_classes.keys()) > 0:
            self._classes = Classes(
                [
                    {"id": key, "name": total_classes[key]}
                    for key in total_classes.keys()
                ]
            )
        self._width, self._height = self.image.size  # type: ignore
        self._free_ram()

    def _initialize_from_wbimage(self, wbimage: "Image") -> None:
        self._grouping = wbimage._grouping
        self._caption = wbimage._caption
        self._width = wbimage._width
        self._height = wbimage._height
        self._image = wbimage._image
        self._classes = wbimage._classes
        self._path = wbimage._path
        self._is_tmp = wbimage._is_tmp
        self._extension = wbimage._extension
        self._sha256 = wbimage._sha256
        self._size = wbimage._size
        self.format = wbimage.format
        self._artifact_source = wbimage._artifact_source
        self._artifact_target = wbimage._artifact_target

        # We do not want to implicitly copy boxes or masks, just the image-related data.
        # self._boxes = wbimage._boxes
        # self._masks = wbimage._masks

    def _initialize_from_path(self, path: str) -> None:
        pil_image = get_module(
            "PIL.Image",
            required='wandb.Image needs the PIL package. To get it, run "pip install pillow".',
        )
        self._set_file(path, is_tmp=False)
        self._image = pil_image.open(path)
        self._image.load()
        ext = os.path.splitext(path)[1][1:]
        self.format = ext

    def _initialize_from_data(self, data: "ImageDataType", mode: str = None,) -> None:
        pil_image = get_module(
            "PIL.Image",
            required='wandb.Image needs the PIL package. To get it, run "pip install pillow".',
        )
        if is_matplotlib_typename(get_full_typename(data)):
            buf = io.BytesIO()
            ensure_matplotlib_figure(data).savefig(buf)
            self._image = pil_image.open(buf)
        elif isinstance(data, pil_image.Image):
            self._image = data
        elif is_pytorch_tensor_typename(get_full_typename(data)):
            vis_util = get_module(
                "torchvision.utils", "torchvision is required to render images"
            )
            if hasattr(data, "requires_grad") and data.requires_grad:
                data = data.detach()
            data = vis_util.make_grid(data, normalize=True)
            self._image = pil_image.fromarray(
                data.mul(255).clamp(0, 255).byte().permute(1, 2, 0).cpu().numpy()
            )
        else:
            if hasattr(data, "numpy"):  # TF data eager tensors
                data = data.numpy()
            if data.ndim > 2:
                data = data.squeeze()  # get rid of trivial dimensions as a convenience
            self._image = pil_image.fromarray(
                self.to_uint8(data), mode=mode or self.guess_mode(data)
            )

        tmp_path = os.path.join(self._MEDIA_TMP.name, str(generate_id()) + ".png")
        self.format = "png"
        self._image.save(tmp_path, transparency=None)
        self._set_file(tmp_path, is_tmp=True)

    @classmethod
    def from_json(
        cls: Type["Image"], json_obj: dict, source_artifact: "PublicArtifact"
    ) -> "Image":
        classes = None
        if json_obj.get("classes") is not None:
            classes = source_artifact.get(json_obj["classes"]["path"])

        masks = json_obj.get("masks")
        _masks: Optional[Dict[str, ImageMask]] = None
        if masks:
            _masks = {}
            for key in masks:
                _masks[key] = ImageMask.from_json(masks[key], source_artifact)
                _masks[key]._set_artifact_source(source_artifact)
                _masks[key]._key = key

        boxes = json_obj.get("boxes")
        _boxes: Optional[Dict[str, BoundingBoxes2D]] = None
        if boxes:
            _boxes = {}
            for key in boxes:
                _boxes[key] = BoundingBoxes2D.from_json(boxes[key], source_artifact)
                _boxes[key]._key = key

        return cls(
            source_artifact.get_path(json_obj["path"]).download(),
            caption=json_obj.get("caption"),
            grouping=json_obj.get("grouping"),
            classes=classes,
            boxes=_boxes,
            masks=_masks,
        )

    @classmethod
    def get_media_subdir(cls: Type["Image"]) -> str:
        return os.path.join("media", "images")

    def bind_to_run(
        self,
        run: "Run",
        key: Union[int, str],
        step: Union[int, str],
        id_: Optional[Union[int, str]] = None,
    ) -> None:
        super().bind_to_run(run, key, step, id_)
        if self._boxes is not None:
            for i, k in enumerate(self._boxes):
                id_ = "{}{}".format(id_, i) if id_ is not None else None
                self._boxes[k].bind_to_run(run, key, step, id_)

        if self._masks is not None:
            for i, k in enumerate(self._masks):
                id_ = "{}{}".format(id_, i) if id_ is not None else None
                self._masks[k].bind_to_run(run, key, step, id_)

    def to_json(self, run_or_artifact: Union["Run", "Artifact"]) -> dict:
        json_dict = super().to_json(run_or_artifact)
        json_dict["_type"] = Image._log_type
        json_dict["format"] = self.format

        if self._width is not None:
            json_dict["width"] = self._width
        if self._height is not None:
            json_dict["height"] = self._height
        if self._grouping:
            json_dict["grouping"] = self._grouping
        if self._caption:
            json_dict["caption"] = self._caption

        if isinstance(run_or_artifact, wandb.sdk.wandb_artifacts.Artifact):
            artifact = run_or_artifact
            if (
                self._masks is not None or self._boxes is not None
            ) and self._classes is None:
                raise ValueError(
                    "classes must be passed to wandb.Image which have masks or bounding boxes when adding to artifacts"
                )

            if self._classes is not None:
                class_id = hashlib.md5(
                    str(self._classes._class_set).encode("utf-8")
                ).hexdigest()
                class_name = os.path.join("media", "classes", class_id + "_cls",)
                classes_entry = artifact.add(self._classes, class_name)
                json_dict["classes"] = {
                    "type": "classes-file",
                    "path": classes_entry.path,
                    "digest": classes_entry.digest,
                }

        elif not isinstance(run_or_artifact, wandb.sdk.wandb_run.Run):
            raise ValueError("to_json accepts wandb_run.Run or wandb_artifact.Artifact")

        if self._boxes:
            json_dict["boxes"] = {
                k: box.to_json(run_or_artifact) for (k, box) in self._boxes.items()
            }
        if self._masks:
            json_dict["masks"] = {
                k: mask.to_json(run_or_artifact) for (k, mask) in self._masks.items()
            }
        return json_dict

    def guess_mode(self, data: "np.ndarray") -> str:
        """
        Guess what type of image the np.array is representing
        """
        # TODO: do we want to support dimensions being at the beginning of the array?
        if data.ndim == 2:
            return "L"
        elif data.shape[-1] == 3:
            return "RGB"
        elif data.shape[-1] == 4:
            return "RGBA"
        else:
            raise ValueError(
                "Un-supported shape for image conversion %s" % list(data.shape)
            )

    @classmethod
    def to_uint8(cls, data: "np.ndarray") -> "np.ndarray":
        """
        Converts floating point image on the range [0,1] and integer images
        on the range [0,255] to uint8, clipping if necessary.
        """
        np = get_module(
            "numpy",
            required="wandb.Image requires numpy if not supplying PIL Images: pip install numpy",
        )

        # I think it's better to check the image range vs the data type, since many
        # image libraries will return floats between 0 and 255

        # some images have range -1...1 or 0-1
        dmin = np.min(data)
        if dmin < 0:
            data = (data - np.min(data)) / np.ptp(data)
        if np.max(data) <= 1.0:
            data = (data * 255).astype(np.int32)

        # assert issubclass(data.dtype.type, np.integer), 'Illegal image format.'
        return data.clip(0, 255).astype(np.uint8)

    @classmethod
    def seq_to_json(
        cls: Type["Image"],
        seq: Sequence["BatchableMedia"],
        run: "Run",
        key: str,
        step: Union[int, str],
    ) -> dict:
        """
        Combines a list of images into a meta dictionary object describing the child images.
        """
        if TYPE_CHECKING:
            seq = cast(Sequence["Image"], seq)

        jsons = [obj.to_json(run) for obj in seq]

        media_dir = cls.get_media_subdir()

        for obj in jsons:
            expected = to_forward_slash_path(media_dir)
            if not obj["path"].startswith(expected):
                raise ValueError(
                    "Files in an array of Image's must be in the {} directory, not {}".format(
                        cls.get_media_subdir(), obj["path"]
                    )
                )

        num_images_to_log = len(seq)
        width, height = seq[0].image.size  # type: ignore
        format = jsons[0]["format"]

        def size_equals_image(image: "Image") -> bool:
            img_width, img_height = image.image.size  # type: ignore
            return img_width == width and img_height == height  # type: ignore

        sizes_match = all(size_equals_image(img) for img in seq)
        if not sizes_match:
            logging.warning(
                "Images sizes do not match. This will causes images to be display incorrectly in the UI."
            )

        meta = {
            "_type": "images/separated",
            "width": width,
            "height": height,
            "format": format,
            "count": num_images_to_log,
        }

        captions = Image.all_captions(seq)

        if captions:
            meta["captions"] = captions

        all_masks = Image.all_masks(seq, run, key, step)

        if all_masks:
            meta["all_masks"] = all_masks

        all_boxes = Image.all_boxes(seq, run, key, step)

        if all_boxes:
            meta["all_boxes"] = all_boxes

        return meta

    @classmethod
    def all_masks(
        cls: Type["Image"],
        images: Sequence["Image"],
        run: "Run",
        run_key: str,
        step: Union[int, str],
    ) -> Union[List[Optional[dict]], bool]:
        all_mask_groups: List[Optional[dict]] = []
        for image in images:
            if image._masks:
                mask_group = {}
                for k in image._masks:
                    mask = image._masks[k]
                    mask_group[k] = mask.to_json(run)
                all_mask_groups.append(mask_group)
            else:
                all_mask_groups.append(None)
        if all_mask_groups and not all(x is None for x in all_mask_groups):
            return all_mask_groups
        else:
            return False

    @classmethod
    def all_boxes(
        cls: Type["Image"],
        images: Sequence["Image"],
        run: "Run",
        run_key: str,
        step: Union[int, str],
    ) -> Union[List[Optional[dict]], bool]:
        all_box_groups: List[Optional[dict]] = []
        for image in images:
            if image._boxes:
                box_group = {}
                for k in image._boxes:
                    box = image._boxes[k]
                    box_group[k] = box.to_json(run)
                all_box_groups.append(box_group)
            else:
                all_box_groups.append(None)
        if all_box_groups and not all(x is None for x in all_box_groups):
            return all_box_groups
        else:
            return False

    @classmethod
    def all_captions(
        cls: Type["Image"], images: Sequence["Media"]
    ) -> Union[bool, Sequence[Optional[str]]]:
        return cls.captions(images)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Image):
            return False
        else:
            self_image = self.image
            other_image = other.image
            if self_image is not None:
                self_image = list(self_image.getdata())
            if other_image is not None:
                other_image = list(other_image.getdata())

            return (
                self._grouping == other._grouping
                and self._caption == other._caption
                and self._width == other._width
                and self._height == other._height
                and self_image == other_image
                and self._classes == other._classes
            )

    def to_data_array(self) -> List[Any]:
        res = []
        if self.image is not None:
            data = list(self.image.getdata())
            for i in range(self.image.height):
                res.append(data[i * self.image.width : (i + 1) * self.image.width])
        self._free_ram()
        return res

    def _free_ram(self) -> None:
        if self._path is not None:
            self._image = None

    @property
    def image(self) -> Optional["PIL.Image"]:
        if self._image is None:
            if self._path is not None:
                pil_image = get_module(
                    "PIL.Image",
                    required='wandb.Image needs the PIL package. To get it, run "pip install pillow".',
                )
                self._image = pil_image.open(self._path)
                self._image.load()
        return self._image


class _ImageFileType(_dtypes.Type):
    name = "image-file"
    legacy_names = ["wandb.Image"]
    types = [Image]

    def __init__(
        self, box_layers=None, box_score_keys=None, mask_layers=None, class_map=None
    ):
        box_layers = box_layers or {}
        box_score_keys = box_score_keys or []
        mask_layers = mask_layers or {}
        class_map = class_map or {}

        if isinstance(box_layers, _dtypes.ConstType):
            box_layers = box_layers._params["val"]
        if not isinstance(box_layers, dict):
            raise TypeError("box_layers must be a dict")
        else:
            box_layers = _dtypes.ConstType(
                {layer_key: set(box_layers[layer_key]) for layer_key in box_layers}
            )

        if isinstance(mask_layers, _dtypes.ConstType):
            mask_layers = mask_layers._params["val"]
        if not isinstance(mask_layers, dict):
            raise TypeError("mask_layers must be a dict")
        else:
            mask_layers = _dtypes.ConstType(
                {layer_key: set(mask_layers[layer_key]) for layer_key in mask_layers}
            )

        if isinstance(box_score_keys, _dtypes.ConstType):
            box_score_keys = box_score_keys._params["val"]
        if not isinstance(box_score_keys, list) and not isinstance(box_score_keys, set):
            raise TypeError("box_score_keys must be a list or a set")
        else:
            box_score_keys = _dtypes.ConstType(set(box_score_keys))

        if isinstance(class_map, _dtypes.ConstType):
            class_map = class_map._params["val"]
        if not isinstance(class_map, dict):
            raise TypeError("class_map must be a dict")
        else:
            class_map = _dtypes.ConstType(class_map)

        self.params.update(
            {
                "box_layers": box_layers,
                "box_score_keys": box_score_keys,
                "mask_layers": mask_layers,
                "class_map": class_map,
            }
        )

    def assign_type(self, wb_type=None):
        if isinstance(wb_type, _ImageFileType):
            box_layers_self = self.params["box_layers"].params["val"] or {}
            box_score_keys_self = self.params["box_score_keys"].params["val"] or []
            mask_layers_self = self.params["mask_layers"].params["val"] or {}
            class_map_self = self.params["class_map"].params["val"] or {}

            box_layers_other = wb_type.params["box_layers"].params["val"] or {}
            box_score_keys_other = wb_type.params["box_score_keys"].params["val"] or []
            mask_layers_other = wb_type.params["mask_layers"].params["val"] or {}
            class_map_other = wb_type.params["class_map"].params["val"] or {}

            # Merge the class_ids from each set of box_layers
            box_layers = {
                str(key): set(
                    list(box_layers_self.get(key, []))
                    + list(box_layers_other.get(key, []))
                )
                for key in set(
                    list(box_layers_self.keys()) + list(box_layers_other.keys())
                )
            }

            # Merge the class_ids from each set of mask_layers
            mask_layers = {
                str(key): set(
                    list(mask_layers_self.get(key, []))
                    + list(mask_layers_other.get(key, []))
                )
                for key in set(
                    list(mask_layers_self.keys()) + list(mask_layers_other.keys())
                )
            }

            # Merge the box score keys
            box_score_keys = set(list(box_score_keys_self) + list(box_score_keys_other))

            # Merge the class_map
            class_map = {
                str(key): class_map_self.get(key, class_map_other.get(key, None))
                for key in set(
                    list(class_map_self.keys()) + list(class_map_other.keys())
                )
            }

            return _ImageFileType(box_layers, box_score_keys, mask_layers, class_map)

        return _dtypes.InvalidType()

    @classmethod
    def from_obj(cls, py_obj):
        if not isinstance(py_obj, Image):
            raise TypeError("py_obj must be a wandb.Image")
        else:
            if hasattr(py_obj, "_boxes") and py_obj._boxes:
                box_layers = {
                    str(key): set(py_obj._boxes[key]._class_labels.keys())
                    for key in py_obj._boxes.keys()
                }
                box_score_keys = set(
                    [
                        key
                        for val in py_obj._boxes.values()
                        for box in val._val
                        for key in box.get("scores", {}).keys()
                    ]
                )

            else:
                box_layers = {}
                box_score_keys = set([])

            if hasattr(py_obj, "_masks") and py_obj._masks:
                mask_layers = {
                    str(key): set(
                        py_obj._masks[key]._val["class_labels"].keys()
                        if hasattr(py_obj._masks[key], "_val")
                        else []
                    )
                    for key in py_obj._masks.keys()
                }
            else:
                mask_layers = {}

            if hasattr(py_obj, "_classes") and py_obj._classes:
                class_set = {
                    str(item["id"]): item["name"] for item in py_obj._classes._class_set
                }
            else:
                class_set = {}

            return cls(box_layers, box_score_keys, mask_layers, class_set)


_dtypes.TypeRegistry.add(_ImageFileType)