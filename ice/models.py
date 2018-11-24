# _*_coding:utf-8_*_
from django.db import models
from .myauth import UserProfile

# Create your models here.

class Asset(models.Model):
    asset_type_choices = (
        ('Server', u"服务器"),
        ('NetworkDevice', u"网络设备"),
        ('SecurityDevice', u"安全设备"),
        ('Software', u"软件资产"),
        ('StorageDevice', u'存储设备'),
        ('other', "其他设备"),
    )

    asset_type = models.CharField(choices=asset_type_choices, max_length=64, verbose_name=u'类型', default="Server")
    name = models.CharField(max_length=64, verbose_name=u'名称', unique=True)
    sn = models.CharField(u'SN号', max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', on_delete=models.CASCADE)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True, on_delete=models.CASCADE)
    trade_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)
    department = models.ForeignKey('Department', verbose_name=u'所属部门', null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name=u'资产标签', blank=True)
    admin = models.ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True, on_delete=models.CASCADE)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True, on_delete=models.CASCADE)

    status_choices = ((0, u'在线'),
                      (1, u'已下线'),
                      (2, u'未知'),
                      (3, u'故障'),
                      (4, u'备用'),
                      )
    status = models.SmallIntegerField(choices=status_choices, verbose_name=u'状态', default=2)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


# class Asset_type(models.Model):
#     asset_type = models.CharField(max_length=64, default='server', unique=True)
#     asset_name = models.CharField(max_length=64)
#
#     def __str__(self):
#         return self.asset_name


class Server(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'PC服务器'),
        (1, u'刀片机'),
        (2, u'小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u"服务器类型", default=0)
    created_by = models.CharField(choices=created_by_choices, max_length=32,
                                  default='auto')  # auto: auto created,   manual:created manually
    # for virtual server
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True,
                                  on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    username = models.CharField(u'系统用户名', max_length=64, blank=True, null=True)
    password = models.CharField(u'系统密码', max_length=64, blank=True, null=True)
    cpu_cord_count = models.SmallIntegerField(u'CPU核数', default=8)
    ram_capacity = models.SmallIntegerField(u'内存大小(G)', default=8)
    disk_capacity = models.IntegerField(u'硬盘大小(G)')
    os_type = models.CharField(verbose_name=u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(verbose_name=u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        # together = ["sn", "asset"]

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)

class Port(models.Model):

    port = models.IntegerField(verbose_name=u'端口号')

    def __str__(self):
        return self.port

class Server_port(models.Model):

    server = models.ForeignKey('Server', on_delete=models.CASCADE)
    port = models.ForeignKey('Port', on_delete=models.CASCADE)

    def __str__(self):
        return self.server.asset.name

class SecurityDevice(models.Model):
    """安全设备"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'防火墙'),
        (1, u'入侵检测设备'),
        (2, u'互联网网关'),
        (4, u'运维审计系统'),
        (5, u'其他'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name="设备类型", default=0)
    config_file = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.asset.id

class NetworkDevice(models.Model):
    """网络设备"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'路由器'),
        (1, u'交换机'),
        (2, u'负载均衡'),
        (4, u'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name="服务器类型", default=0)
    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software', blank=True, null=True, on_delete=models.CASCADE)
    port_num = models.SmallIntegerField(u'端口个数', null=True, blank=True)
    config_file = models.TextField(u'设置详细配置', null=True, blank=True)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"

class Software(models.Model):
    '''
    only save software which purchased
    '''
    sub_asset_type_choices = (
        (0, u'OS'),
        (1, u'办公\开发软件'),
        (2, u'业务软件'),

    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name="软件类型", default=0)
    license_num = models.IntegerField(verbose_name="授权数")
    # os_distribution_choices = (('windows','Windows'),
    #                            ('centos','CentOS'),
    #                            ('ubuntu', 'Ubuntu'))
    # type = models.CharField(u'系统类型', choices=os_types_choice, max_length=64,help_text=u'eg. GNU/Linux',default=1)
    # distribution = models.CharField(u'发型版本', choices=os_distribution_choices,max_length=32,default='windows')
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)

    # language_choices = (('cn',u'中文'),
    #                     ('en',u'英文'))
    # language = models.CharField(u'系统语言',choices = language_choices, default='cn',max_length=32)
    # #version = models.CharField(u'版本号', max_length=64,help_text=u'2.6.32-431.3.1.el6.x86_64' )

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"

class Manufactory(models.Model):
    """厂商"""

    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_man = models.CharField(u'联系人', max_length=30, blank=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"

class Department(models.Model):
    """部门"""

    name = models.CharField(u'部门名称', max_length=64, unique=True)
    director = models.ForeignKey('UserProfile', on_delete=models.CASCADE,)
    # contact = models.ForeignKey('UserProfile',default=None)
    memo = models.CharField(u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = "部门"


class Contract(models.Model):
    """合同"""

    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    file = models.FileField(u'合同文件', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __str__(self):
        return self.name

class IDC(models.Model):
    """机房"""

    name = models.CharField(u'机房名称', max_length=64, unique=True)
    location = models.CharField(u'机房位置', max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

