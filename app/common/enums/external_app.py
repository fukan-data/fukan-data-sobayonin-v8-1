from common.enums.base_enum import BaseEnum


class ExternalApp(BaseEnum):
    EMAIL = (0, 'メール', 'email')
    SLACK = (1, 'スラック', 'slack')
    LINE = (2, 'ライン', 'line')
    FACEBOOK = (3, 'フェイスブック', 'facebook')
    INSTAGRAM = (4, 'インスタグラム', 'instagram')
