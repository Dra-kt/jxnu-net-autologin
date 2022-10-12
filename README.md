### 使用方法

1. 将账号密码与运营商信息填入`username.json`配置文件中
2. 启动程序

### Windows计划任务事件

可以利用Windows计划任务自动化登陆，所使用的计划触发器规则：

```
<QueryList>
 <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
  <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">*[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig']and(EventID=8001)]][EventData[Data[@Name='SSID']='jxnu_stu']]</Select>
 </Query>
</QueryList>
```

