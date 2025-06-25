class ProteinVisualizationResponse:
    def __init__(self, code: int, modelUrl: str, message: str, metadata: dict):
        self.code = code
        self.modelUrl = modelUrl
        self.message = message
        self.metadata = metadata

    def to_dict(self):
        return {
            'code': self.code,
            'modelUrl': self.modelUrl,
            'message': self.message,
            'metadata': self.metadata
        }

class ResultResponse:
    def __init__(self, code: int, message: str, metadata: dict):
        self.code = code
        self.message = message  # 正确接收参数
        self.metadata = metadata

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'metadata': self.metadata,
        }