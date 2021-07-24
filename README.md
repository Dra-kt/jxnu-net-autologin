### 使用方法

讲账号密码等信息填入username.json配置文件中，启动程序即可，登陆操作会在后台完成

注：配置文件使用json格式

### Windows计划任务事件

可以利用Windows计划任务自动化登陆操作，说使用的计划触发器规则：

```
<QueryList>
 <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
  <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">*[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig']and(EventID=8001)]][EventData[Data[@Name='SSID']='jxnu_stu']]</Select>
 </Query>
</QueryList>
```

