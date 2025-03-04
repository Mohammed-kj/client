"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions
import wandb.proto.wandb_base_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class TelemetryRecord(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    IMPORTS_INIT_FIELD_NUMBER: builtins.int
    IMPORTS_FINISH_FIELD_NUMBER: builtins.int
    FEATURE_FIELD_NUMBER: builtins.int
    PYTHON_VERSION_FIELD_NUMBER: builtins.int
    CLI_VERSION_FIELD_NUMBER: builtins.int
    HUGGINGFACE_VERSION_FIELD_NUMBER: builtins.int
    ENV_FIELD_NUMBER: builtins.int
    LABEL_FIELD_NUMBER: builtins.int
    DEPRECATED_FIELD_NUMBER: builtins.int
    ISSUES_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    python_version: typing.Text = ...
    cli_version: typing.Text = ...
    huggingface_version: typing.Text = ...

    @property
    def imports_init(self) -> global___Imports: ...

    @property
    def imports_finish(self) -> global___Imports: ...

    @property
    def feature(self) -> global___Feature: ...

    @property
    def env(self) -> global___Env: ...

    @property
    def label(self) -> global___Labels: ...

    @property
    def deprecated(self) -> global___Deprecated: ...

    @property
    def issues(self) -> global___Issues: ...

    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...

    def __init__(self,
        *,
        imports_init : typing.Optional[global___Imports] = ...,
        imports_finish : typing.Optional[global___Imports] = ...,
        feature : typing.Optional[global___Feature] = ...,
        python_version : typing.Text = ...,
        cli_version : typing.Text = ...,
        huggingface_version : typing.Text = ...,
        env : typing.Optional[global___Env] = ...,
        label : typing.Optional[global___Labels] = ...,
        deprecated : typing.Optional[global___Deprecated] = ...,
        issues : typing.Optional[global___Issues] = ...,
        _info : typing.Optional[wandb.proto.wandb_base_pb2._RecordInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"_info",b"_info",u"deprecated",b"deprecated",u"env",b"env",u"feature",b"feature",u"imports_finish",b"imports_finish",u"imports_init",b"imports_init",u"issues",b"issues",u"label",b"label"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"_info",b"_info",u"cli_version",b"cli_version",u"deprecated",b"deprecated",u"env",b"env",u"feature",b"feature",u"huggingface_version",b"huggingface_version",u"imports_finish",b"imports_finish",u"imports_init",b"imports_init",u"issues",b"issues",u"label",b"label",u"python_version",b"python_version"]) -> None: ...
global___TelemetryRecord = TelemetryRecord

class TelemetryResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...

    def __init__(self,
        ) -> None: ...
global___TelemetryResult = TelemetryResult

class Imports(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    TORCH_FIELD_NUMBER: builtins.int
    KERAS_FIELD_NUMBER: builtins.int
    TENSORFLOW_FIELD_NUMBER: builtins.int
    FASTAI_FIELD_NUMBER: builtins.int
    SKLEARN_FIELD_NUMBER: builtins.int
    XGBOOST_FIELD_NUMBER: builtins.int
    CATBOOST_FIELD_NUMBER: builtins.int
    LIGHTGBM_FIELD_NUMBER: builtins.int
    PYTORCH_LIGHTNING_FIELD_NUMBER: builtins.int
    PYTORCH_IGNITE_FIELD_NUMBER: builtins.int
    TRANSFORMERS_HUGGINGFACE_FIELD_NUMBER: builtins.int
    JAX_FIELD_NUMBER: builtins.int
    METAFLOW_FIELD_NUMBER: builtins.int
    ALLENNLP_FIELD_NUMBER: builtins.int
    AUTOGLUON_FIELD_NUMBER: builtins.int
    AUTOKERAS_FIELD_NUMBER: builtins.int
    CATALYST_FIELD_NUMBER: builtins.int
    DEEPCHEM_FIELD_NUMBER: builtins.int
    DEEPCTR_FIELD_NUMBER: builtins.int
    PYCARET_FIELD_NUMBER: builtins.int
    PYTORCHVIDEO_FIELD_NUMBER: builtins.int
    RAY_FIELD_NUMBER: builtins.int
    SIMPLETRANSFORMERS_FIELD_NUMBER: builtins.int
    SKORCH_FIELD_NUMBER: builtins.int
    SPACY_FIELD_NUMBER: builtins.int
    FLASH_FIELD_NUMBER: builtins.int
    OPTUNA_FIELD_NUMBER: builtins.int
    RECBOLE_FIELD_NUMBER: builtins.int
    MMCV_FIELD_NUMBER: builtins.int
    MMDET_FIELD_NUMBER: builtins.int
    TORCHDRUG_FIELD_NUMBER: builtins.int
    TORCHTEXT_FIELD_NUMBER: builtins.int
    TORCHVISION_FIELD_NUMBER: builtins.int
    ELEGY_FIELD_NUMBER: builtins.int
    DETECTRON2_FIELD_NUMBER: builtins.int
    FLAIR_FIELD_NUMBER: builtins.int
    FLAX_FIELD_NUMBER: builtins.int
    SYFT_FIELD_NUMBER: builtins.int
    TTS_FIELD_NUMBER: builtins.int
    MONAI_FIELD_NUMBER: builtins.int
    HUGGINGFACE_HUB_FIELD_NUMBER: builtins.int
    HYDRA_FIELD_NUMBER: builtins.int
    DATASETS_FIELD_NUMBER: builtins.int
    SACRED_FIELD_NUMBER: builtins.int
    JOBLIB_FIELD_NUMBER: builtins.int
    DASK_FIELD_NUMBER: builtins.int
    ASYNCIO_FIELD_NUMBER: builtins.int
    torch: builtins.bool = ...
    keras: builtins.bool = ...
    tensorflow: builtins.bool = ...
    fastai: builtins.bool = ...
    sklearn: builtins.bool = ...
    xgboost: builtins.bool = ...
    catboost: builtins.bool = ...
    lightgbm: builtins.bool = ...
    pytorch_lightning: builtins.bool = ...
    pytorch_ignite: builtins.bool = ...
    transformers_huggingface: builtins.bool = ...
    jax: builtins.bool = ...
    metaflow: builtins.bool = ...
    allennlp: builtins.bool = ...
    autogluon: builtins.bool = ...
    autokeras: builtins.bool = ...
    catalyst: builtins.bool = ...
    deepchem: builtins.bool = ...
    deepctr: builtins.bool = ...
    pycaret: builtins.bool = ...
    pytorchvideo: builtins.bool = ...
    ray: builtins.bool = ...
    simpletransformers: builtins.bool = ...
    skorch: builtins.bool = ...
    spacy: builtins.bool = ...
    flash: builtins.bool = ...
    optuna: builtins.bool = ...
    recbole: builtins.bool = ...
    mmcv: builtins.bool = ...
    mmdet: builtins.bool = ...
    torchdrug: builtins.bool = ...
    torchtext: builtins.bool = ...
    torchvision: builtins.bool = ...
    elegy: builtins.bool = ...
    detectron2: builtins.bool = ...
    flair: builtins.bool = ...
    flax: builtins.bool = ...
    syft: builtins.bool = ...
    TTS: builtins.bool = ...
    monai: builtins.bool = ...
    huggingface_hub: builtins.bool = ...
    hydra: builtins.bool = ...
    datasets: builtins.bool = ...
    sacred: builtins.bool = ...
    joblib: builtins.bool = ...
    dask: builtins.bool = ...
    asyncio: builtins.bool = ...

    def __init__(self,
        *,
        torch : builtins.bool = ...,
        keras : builtins.bool = ...,
        tensorflow : builtins.bool = ...,
        fastai : builtins.bool = ...,
        sklearn : builtins.bool = ...,
        xgboost : builtins.bool = ...,
        catboost : builtins.bool = ...,
        lightgbm : builtins.bool = ...,
        pytorch_lightning : builtins.bool = ...,
        pytorch_ignite : builtins.bool = ...,
        transformers_huggingface : builtins.bool = ...,
        jax : builtins.bool = ...,
        metaflow : builtins.bool = ...,
        allennlp : builtins.bool = ...,
        autogluon : builtins.bool = ...,
        autokeras : builtins.bool = ...,
        catalyst : builtins.bool = ...,
        deepchem : builtins.bool = ...,
        deepctr : builtins.bool = ...,
        pycaret : builtins.bool = ...,
        pytorchvideo : builtins.bool = ...,
        ray : builtins.bool = ...,
        simpletransformers : builtins.bool = ...,
        skorch : builtins.bool = ...,
        spacy : builtins.bool = ...,
        flash : builtins.bool = ...,
        optuna : builtins.bool = ...,
        recbole : builtins.bool = ...,
        mmcv : builtins.bool = ...,
        mmdet : builtins.bool = ...,
        torchdrug : builtins.bool = ...,
        torchtext : builtins.bool = ...,
        torchvision : builtins.bool = ...,
        elegy : builtins.bool = ...,
        detectron2 : builtins.bool = ...,
        flair : builtins.bool = ...,
        flax : builtins.bool = ...,
        syft : builtins.bool = ...,
        TTS : builtins.bool = ...,
        monai : builtins.bool = ...,
        huggingface_hub : builtins.bool = ...,
        hydra : builtins.bool = ...,
        datasets : builtins.bool = ...,
        sacred : builtins.bool = ...,
        joblib : builtins.bool = ...,
        dask : builtins.bool = ...,
        asyncio : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"TTS",b"TTS",u"allennlp",b"allennlp",u"asyncio",b"asyncio",u"autogluon",b"autogluon",u"autokeras",b"autokeras",u"catalyst",b"catalyst",u"catboost",b"catboost",u"dask",b"dask",u"datasets",b"datasets",u"deepchem",b"deepchem",u"deepctr",b"deepctr",u"detectron2",b"detectron2",u"elegy",b"elegy",u"fastai",b"fastai",u"flair",b"flair",u"flash",b"flash",u"flax",b"flax",u"huggingface_hub",b"huggingface_hub",u"hydra",b"hydra",u"jax",b"jax",u"joblib",b"joblib",u"keras",b"keras",u"lightgbm",b"lightgbm",u"metaflow",b"metaflow",u"mmcv",b"mmcv",u"mmdet",b"mmdet",u"monai",b"monai",u"optuna",b"optuna",u"pycaret",b"pycaret",u"pytorch_ignite",b"pytorch_ignite",u"pytorch_lightning",b"pytorch_lightning",u"pytorchvideo",b"pytorchvideo",u"ray",b"ray",u"recbole",b"recbole",u"sacred",b"sacred",u"simpletransformers",b"simpletransformers",u"sklearn",b"sklearn",u"skorch",b"skorch",u"spacy",b"spacy",u"syft",b"syft",u"tensorflow",b"tensorflow",u"torch",b"torch",u"torchdrug",b"torchdrug",u"torchtext",b"torchtext",u"torchvision",b"torchvision",u"transformers_huggingface",b"transformers_huggingface",u"xgboost",b"xgboost"]) -> None: ...
global___Imports = Imports

class Feature(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    WATCH_FIELD_NUMBER: builtins.int
    FINISH_FIELD_NUMBER: builtins.int
    SAVE_FIELD_NUMBER: builtins.int
    OFFLINE_FIELD_NUMBER: builtins.int
    RESUMED_FIELD_NUMBER: builtins.int
    GRPC_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    KERAS_FIELD_NUMBER: builtins.int
    SAGEMAKER_FIELD_NUMBER: builtins.int
    ARTIFACT_INCREMENTAL_FIELD_NUMBER: builtins.int
    METAFLOW_FIELD_NUMBER: builtins.int
    PRODIGY_FIELD_NUMBER: builtins.int
    SET_INIT_NAME_FIELD_NUMBER: builtins.int
    SET_INIT_ID_FIELD_NUMBER: builtins.int
    SET_INIT_TAGS_FIELD_NUMBER: builtins.int
    SET_INIT_CONFIG_FIELD_NUMBER: builtins.int
    SET_RUN_NAME_FIELD_NUMBER: builtins.int
    SET_RUN_TAGS_FIELD_NUMBER: builtins.int
    SET_CONFIG_ITEM_FIELD_NUMBER: builtins.int
    LAUNCH_FIELD_NUMBER: builtins.int
    TORCH_PROFILER_TRACE_FIELD_NUMBER: builtins.int
    SB3_FIELD_NUMBER: builtins.int
    SERVICE_FIELD_NUMBER: builtins.int
    INIT_RETURN_RUN_FIELD_NUMBER: builtins.int
    LIGHTGBM_WANDB_CALLBACK_FIELD_NUMBER: builtins.int
    LIGHTGBM_LOG_SUMMARY_FIELD_NUMBER: builtins.int
    CATBOOST_WANDB_CALLBACK_FIELD_NUMBER: builtins.int
    CATBOOST_LOG_SUMMARY_FIELD_NUMBER: builtins.int
    TENSORBOARD_LOG_FIELD_NUMBER: builtins.int
    ESTIMATOR_HOOK_FIELD_NUMBER: builtins.int
    XGBOOST_WANDB_CALLBACK_FIELD_NUMBER: builtins.int
    XGBOOST_OLD_WANDB_CALLBACK_FIELD_NUMBER: builtins.int
    ATTACH_FIELD_NUMBER: builtins.int
    TENSORBOARD_PATCH_FIELD_NUMBER: builtins.int
    TENSORBOARD_SYNC_FIELD_NUMBER: builtins.int
    KFP_WANDB_LOG_FIELD_NUMBER: builtins.int
    watch: builtins.bool = ...
    finish: builtins.bool = ...
    save: builtins.bool = ...
    offline: builtins.bool = ...
    resumed: builtins.bool = ...
    grpc: builtins.bool = ...
    metric: builtins.bool = ...
    keras: builtins.bool = ...
    sagemaker: builtins.bool = ...
    artifact_incremental: builtins.bool = ...
    metaflow: builtins.bool = ...
    prodigy: builtins.bool = ...
    set_init_name: builtins.bool = ...
    set_init_id: builtins.bool = ...
    set_init_tags: builtins.bool = ...
    set_init_config: builtins.bool = ...
    set_run_name: builtins.bool = ...
    set_run_tags: builtins.bool = ...
    set_config_item: builtins.bool = ...
    launch: builtins.bool = ...
    torch_profiler_trace: builtins.bool = ...
    sb3: builtins.bool = ...
    service: builtins.bool = ...
    init_return_run: builtins.bool = ...
    lightgbm_wandb_callback: builtins.bool = ...
    lightgbm_log_summary: builtins.bool = ...
    catboost_wandb_callback: builtins.bool = ...
    catboost_log_summary: builtins.bool = ...
    tensorboard_log: builtins.bool = ...
    estimator_hook: builtins.bool = ...
    xgboost_wandb_callback: builtins.bool = ...
    xgboost_old_wandb_callback: builtins.bool = ...
    attach: builtins.bool = ...
    tensorboard_patch: builtins.bool = ...
    tensorboard_sync: builtins.bool = ...
    kfp_wandb_log: builtins.bool = ...

    def __init__(self,
        *,
        watch : builtins.bool = ...,
        finish : builtins.bool = ...,
        save : builtins.bool = ...,
        offline : builtins.bool = ...,
        resumed : builtins.bool = ...,
        grpc : builtins.bool = ...,
        metric : builtins.bool = ...,
        keras : builtins.bool = ...,
        sagemaker : builtins.bool = ...,
        artifact_incremental : builtins.bool = ...,
        metaflow : builtins.bool = ...,
        prodigy : builtins.bool = ...,
        set_init_name : builtins.bool = ...,
        set_init_id : builtins.bool = ...,
        set_init_tags : builtins.bool = ...,
        set_init_config : builtins.bool = ...,
        set_run_name : builtins.bool = ...,
        set_run_tags : builtins.bool = ...,
        set_config_item : builtins.bool = ...,
        launch : builtins.bool = ...,
        torch_profiler_trace : builtins.bool = ...,
        sb3 : builtins.bool = ...,
        service : builtins.bool = ...,
        init_return_run : builtins.bool = ...,
        lightgbm_wandb_callback : builtins.bool = ...,
        lightgbm_log_summary : builtins.bool = ...,
        catboost_wandb_callback : builtins.bool = ...,
        catboost_log_summary : builtins.bool = ...,
        tensorboard_log : builtins.bool = ...,
        estimator_hook : builtins.bool = ...,
        xgboost_wandb_callback : builtins.bool = ...,
        xgboost_old_wandb_callback : builtins.bool = ...,
        attach : builtins.bool = ...,
        tensorboard_patch : builtins.bool = ...,
        tensorboard_sync : builtins.bool = ...,
        kfp_wandb_log : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"artifact_incremental",b"artifact_incremental",u"attach",b"attach",u"catboost_log_summary",b"catboost_log_summary",u"catboost_wandb_callback",b"catboost_wandb_callback",u"estimator_hook",b"estimator_hook",u"finish",b"finish",u"grpc",b"grpc",u"init_return_run",b"init_return_run",u"keras",b"keras",u"kfp_wandb_log",b"kfp_wandb_log",u"launch",b"launch",u"lightgbm_log_summary",b"lightgbm_log_summary",u"lightgbm_wandb_callback",b"lightgbm_wandb_callback",u"metaflow",b"metaflow",u"metric",b"metric",u"offline",b"offline",u"prodigy",b"prodigy",u"resumed",b"resumed",u"sagemaker",b"sagemaker",u"save",b"save",u"sb3",b"sb3",u"service",b"service",u"set_config_item",b"set_config_item",u"set_init_config",b"set_init_config",u"set_init_id",b"set_init_id",u"set_init_name",b"set_init_name",u"set_init_tags",b"set_init_tags",u"set_run_name",b"set_run_name",u"set_run_tags",b"set_run_tags",u"tensorboard_log",b"tensorboard_log",u"tensorboard_patch",b"tensorboard_patch",u"tensorboard_sync",b"tensorboard_sync",u"torch_profiler_trace",b"torch_profiler_trace",u"watch",b"watch",u"xgboost_old_wandb_callback",b"xgboost_old_wandb_callback",u"xgboost_wandb_callback",b"xgboost_wandb_callback"]) -> None: ...
global___Feature = Feature

class Env(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    JUPYTER_FIELD_NUMBER: builtins.int
    KAGGLE_FIELD_NUMBER: builtins.int
    WINDOWS_FIELD_NUMBER: builtins.int
    M1_GPU_FIELD_NUMBER: builtins.int
    START_SPAWN_FIELD_NUMBER: builtins.int
    START_FORK_FIELD_NUMBER: builtins.int
    START_FORKSERVER_FIELD_NUMBER: builtins.int
    START_THREAD_FIELD_NUMBER: builtins.int
    MAYBE_MP_FIELD_NUMBER: builtins.int
    jupyter: builtins.bool = ...
    kaggle: builtins.bool = ...
    windows: builtins.bool = ...
    m1_gpu: builtins.bool = ...
    start_spawn: builtins.bool = ...
    start_fork: builtins.bool = ...
    start_forkserver: builtins.bool = ...
    start_thread: builtins.bool = ...
    maybe_mp: builtins.bool = ...

    def __init__(self,
        *,
        jupyter : builtins.bool = ...,
        kaggle : builtins.bool = ...,
        windows : builtins.bool = ...,
        m1_gpu : builtins.bool = ...,
        start_spawn : builtins.bool = ...,
        start_fork : builtins.bool = ...,
        start_forkserver : builtins.bool = ...,
        start_thread : builtins.bool = ...,
        maybe_mp : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"jupyter",b"jupyter",u"kaggle",b"kaggle",u"m1_gpu",b"m1_gpu",u"maybe_mp",b"maybe_mp",u"start_fork",b"start_fork",u"start_forkserver",b"start_forkserver",u"start_spawn",b"start_spawn",u"start_thread",b"start_thread",u"windows",b"windows"]) -> None: ...
global___Env = Env

class Labels(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CODE_STRING_FIELD_NUMBER: builtins.int
    REPO_STRING_FIELD_NUMBER: builtins.int
    CODE_VERSION_FIELD_NUMBER: builtins.int
    code_string: typing.Text = ...
    repo_string: typing.Text = ...
    code_version: typing.Text = ...

    def __init__(self,
        *,
        code_string : typing.Text = ...,
        repo_string : typing.Text = ...,
        code_version : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"code_string",b"code_string",u"code_version",b"code_version",u"repo_string",b"repo_string"]) -> None: ...
global___Labels = Labels

class Deprecated(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    KERAS_CALLBACK__DATA_TYPE_FIELD_NUMBER: builtins.int
    RUN__MODE_FIELD_NUMBER: builtins.int
    RUN__SAVE_NO_ARGS_FIELD_NUMBER: builtins.int
    RUN__JOIN_FIELD_NUMBER: builtins.int
    PLOTS_FIELD_NUMBER: builtins.int
    RUN__LOG_SYNC_FIELD_NUMBER: builtins.int
    keras_callback__data_type: builtins.bool = ...
    run__mode: builtins.bool = ...
    run__save_no_args: builtins.bool = ...
    run__join: builtins.bool = ...
    plots: builtins.bool = ...
    run__log_sync: builtins.bool = ...

    def __init__(self,
        *,
        keras_callback__data_type : builtins.bool = ...,
        run__mode : builtins.bool = ...,
        run__save_no_args : builtins.bool = ...,
        run__join : builtins.bool = ...,
        plots : builtins.bool = ...,
        run__log_sync : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"keras_callback__data_type",b"keras_callback__data_type",u"plots",b"plots",u"run__join",b"run__join",u"run__log_sync",b"run__log_sync",u"run__mode",b"run__mode",u"run__save_no_args",b"run__save_no_args"]) -> None: ...
global___Deprecated = Deprecated

class Issues(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SETTINGS__VALIDATION_WARNINGS_FIELD_NUMBER: builtins.int
    SETTINGS__UNEXPECTED_ARGS_FIELD_NUMBER: builtins.int
    SETTINGS__PREPROCESSING_WARNINGS_FIELD_NUMBER: builtins.int
    settings__validation_warnings: builtins.bool = ...
    settings__unexpected_args: builtins.bool = ...
    settings__preprocessing_warnings: builtins.bool = ...

    def __init__(self,
        *,
        settings__validation_warnings : builtins.bool = ...,
        settings__unexpected_args : builtins.bool = ...,
        settings__preprocessing_warnings : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"settings__preprocessing_warnings",b"settings__preprocessing_warnings",u"settings__unexpected_args",b"settings__unexpected_args",u"settings__validation_warnings",b"settings__validation_warnings"]) -> None: ...
global___Issues = Issues
