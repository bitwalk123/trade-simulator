class AppRes:
    path_conf = 'conf'
    path_image = 'images'
    path_info = 'info'

    def getConfigDir(self) -> str:
        return self.path_conf

    def getImageDir(self) -> str:
        return self.path_image

    def getInfoDir(self) -> str:
        return self.path_info
