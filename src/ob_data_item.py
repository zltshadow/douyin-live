class ObDataItem:
    # 类变量，用于存储当前最大的ID值
    current_id = 0

    def __init__(self, nickname, gender, account, message_type, message_content, profile_url=None):
        # 调用类方法获取下一个自增的ID值
        self.id = ObDataItem.get_next_id()
        self.nickname = nickname
        self.gender = gender
        self.account = account
        self.message_type = message_type
        self.message_content = message_content
        self.profile_url = profile_url

    @classmethod
    def get_next_id(cls):
        # 类方法用于获取下一个自增的ID值，并更新类变量
        cls.current_id += 1
        return cls.current_id

    @classmethod
    def reset_id(cls):
        # 类方法用于归零ID
        cls.current_id = 0

    def to_array(self):
        # 将实例的所有属性转为数组
        return [self.id, self.nickname, self.gender, self.account, self.message_type, self.message_content,
                self.profile_url]
