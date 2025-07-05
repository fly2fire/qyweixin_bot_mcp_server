# 企业微信模版卡片类型(template_card)规范

## 消息类型概述
模版卡片消息类型用于发送结构化的卡片消息，支持丰富的内容展示和交互功能。提供两种卡片类型：
- **text_notice** - 文本通知模版卡片
- **news_notice** - 图文展示模版卡片

## 卡片类型对比

| 特性 | 文本通知模版卡片 | 图文展示模版卡片 |
|------|------------------|------------------|
| 卡片类型 | text_notice | news_notice |
| 主要用途 | 文本通知、数据展示 | 图文展示、内容推广 |
| 关键数据 | 支持 emphasis_content | 不支持 |
| 卡片图片 | 不支持 | 支持 card_image |
| 左图右文 | 不支持 | 支持 image_text_area |
| 垂直内容 | 不支持 | 支持 vertical_content_list |
| 二级文本 | 支持 sub_title_text | 不支持 |

## 文本通知模版卡片 (text_notice)

### JSON 结构
```json
{
    "msgtype":"template_card",
    "template_card":{
        "card_type":"text_notice",
        "source":{
            "icon_url":"https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
            "desc":"企业微信",
            "desc_color":0
        },
        "main_title":{
            "title":"欢迎使用企业微信",
            "desc":"您的好友正在邀请您加入企业微信"
        },
        "emphasis_content":{
            "title":"100",
            "desc":"数据含义"
        },
        "quote_area":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH",
            "title":"引用文本标题",
            "quote_text":"Jack：企业微信真的很好用~\nBalian：超级好的一款软件！"
        },
        "sub_title_text":"下载企业微信还能抢红包！",
        "horizontal_content_list":[
            {
                "keyname":"邀请人",
                "value":"张三"
            },
            {
                "keyname":"企微官网",
                "value":"点击访问",
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi"
            },
            {
                "keyname":"企微下载",
                "value":"企业微信.apk",
                "type":2,
                "media_id":"MEDIAID"
            }
        ],
        "jump_list":[
            {
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi",
                "title":"企业微信官网"
            },
            {
                "type":2,
                "appid":"APPID",
                "pagepath":"PAGEPATH",
                "title":"跳转小程序"
            }
        ],
        "card_action":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH"
        }
    }
}
```

### 参数说明

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| msgtype | String | 是 | 消息类型，此时的消息类型固定为template_card |
| template_card | Object | 是 | 具体的模版卡片参数 |
| card_type | String | 是 | 模版卡片的模版类型，文本通知模版卡片的类型为text_notice |
| source | Object | 否 | 卡片来源样式信息，不需要来源样式可不填写 |
| source.icon_url | String | 否 | 来源图片的url |
| source.desc | String | 否 | 来源图片的描述，建议不超过13个字 |
| source.desc_color | Int | 否 | 来源文字的颜色，目前支持：0(默认) 灰色，1 黑色，2 红色，3 绿色 |
| main_title | Object | 是 | 模版卡片的主要内容，包括一级标题和标题辅助信息 |
| main_title.title | String | 否 | 一级标题，建议不超过26个字。模版卡片主要内容的一级标题main_title.title和二级普通文本sub_title_text必须有一项填写 |
| main_title.desc | String | 否 | 标题辅助信息，建议不超过30个字 |
| emphasis_content | Object | 否 | 关键数据样式 |
| emphasis_content.title | String | 否 | 关键数据样式的数据内容，建议不超过10个字 |
| emphasis_content.desc | String | 否 | 关键数据样式的数据描述内容，建议不超过15个字 |
| quote_area | Object | 否 | 引用文献样式，建议不与关键数据共用 |
| quote_area.type | Int | 否 | 引用文献样式区域点击事件，0或不填代表没有点击事件，1 代表跳转url，2 代表跳转小程序 |
| quote_area.url | String | 否 | 点击跳转的url，quote_area.type是1时必填 |
| quote_area.appid | String | 否 | 点击跳转的小程序的appid，quote_area.type是2时必填 |
| quote_area.pagepath | String | 否 | 点击跳转的小程序的pagepath，quote_area.type是2时选填 |
| quote_area.title | String | 否 | 引用文献样式的标题 |
| quote_area.quote_text | String | 否 | 引用文献样式的引用文案 |
| sub_title_text | String | 否 | 二级普通文本，建议不超过112个字。模版卡片主要内容的一级标题main_title.title和二级普通文本sub_title_text必须有一项填写 |
| horizontal_content_list | Object[] | 否 | 二级标题+文本列表，该字段可为空数组，但有数据的话需确认对应字段是否必填，列表长度不超过6 |
| horizontal_content_list.type | Int | 否 | 模版卡片的二级标题信息内容支持的类型，1是url，2是文件附件，3 代表点击跳转成员详情 |
| horizontal_content_list.keyname | String | 是 | 二级标题，建议不超过5个字 |
| horizontal_content_list.value | String | 否 | 二级文本，如果horizontal_content_list.type是2，该字段代表文件名称（要包含文件类型），建议不超过26个字 |
| horizontal_content_list.url | String | 否 | 链接跳转的url，horizontal_content_list.type是1时必填 |
| horizontal_content_list.media_id | String | 否 | 附件的media_id，horizontal_content_list.type是2时必填 |
| horizontal_content_list.userid | String | 否 | 成员详情的userid，horizontal_content_list.type是3时必填 |
| jump_list | Object[] | 否 | 跳转指引样式的列表，该字段可为空数组，但有数据的话需确认对应字段是否必填，列表长度不超过3 |
| jump_list.type | Int | 否 | 跳转链接类型，0或不填代表不是链接，1 代表跳转url，2 代表跳转小程序 |
| jump_list.title | String | 是 | 跳转链接样式的文案内容，建议不超过13个字 |
| jump_list.url | String | 否 | 跳转链接的url，jump_list.type是1时必填 |
| jump_list.appid | String | 否 | 跳转链接的小程序的appid，jump_list.type是2时必填 |
| jump_list.pagepath | String | 否 | 跳转链接的小程序的pagepath，jump_list.type是2时选填 |
| card_action | Object | 是 | 整体卡片的点击跳转事件，text_notice模版卡片中该字段为必填项 |
| card_action.type | Int | 是 | 卡片跳转类型，1 代表跳转url，2 代表打开小程序。text_notice模版卡片中该字段取值范围为[1,2] |
| card_action.url | String | 否 | 跳转事件的url，card_action.type是1时必填 |
| card_action.appid | String | 否 | 跳转事件的小程序的appid，card_action.type是2时必填 |
| card_action.pagepath | String | 否 | 跳转事件的小程序的pagepath，card_action.type是2时选填 |

## 图文展示模版卡片 (news_notice)

### JSON 结构
```json
{
    "msgtype":"template_card",
    "template_card":{
        "card_type":"news_notice",
        "source":{
            "icon_url":"https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
            "desc":"企业微信",
            "desc_color":0
        },
        "main_title":{
            "title":"欢迎使用企业微信",
            "desc":"您的好友正在邀请您加入企业微信"
        },
        "card_image":{
            "url":"https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0",
            "aspect_ratio":2.25
        },
        "image_text_area":{
            "type":1,
            "url":"https://work.weixin.qq.com",
            "title":"欢迎使用企业微信",
            "desc":"您的好友正在邀请您加入企业微信",
            "image_url":"https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0"
        },
        "quote_area":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH",
            "title":"引用文本标题",
            "quote_text":"Jack：企业微信真的很好用~\nBalian：超级好的一款软件！"
        },
        "vertical_content_list":[
            {
                "title":"惊喜红包等你来拿",
                "desc":"下载企业微信还能抢红包！"
            }
        ],
        "horizontal_content_list":[
            {
                "keyname":"邀请人",
                "value":"张三"
            },
            {
                "keyname":"企微官网",
                "value":"点击访问",
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi"
            },
            {
                "keyname":"企微下载",
                "value":"企业微信.apk",
                "type":2,
                "media_id":"MEDIAID"
            }
        ],
        "jump_list":[
            {
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi",
                "title":"企业微信官网"
            },
            {
                "type":2,
                "appid":"APPID",
                "pagepath":"PAGEPATH",
                "title":"跳转小程序"
            }
        ],
        "card_action":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH"
        }
    }
}
```

### 参数说明

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| msgtype | String | 是 | 模版卡片的消息类型为template_card |
| template_card | Object | 是 | 具体的模版卡片参数 |
| card_type | String | 是 | 模版卡片的模版类型，图文展示模版卡片的类型为news_notice |
| source | Object | 否 | 卡片来源样式信息，不需要来源样式可不填写 |
| source.icon_url | String | 否 | 来源图片的url |
| source.desc | String | 否 | 来源图片的描述，建议不超过13个字 |
| source.desc_color | Int | 否 | 来源文字的颜色，目前支持：0(默认) 灰色，1 黑色，2 红色，3 绿色 |
| main_title | Object | 是 | 模版卡片的主要内容，包括一级标题和标题辅助信息 |
| main_title.title | String | 是 | 一级标题，建议不超过26个字 |
| main_title.desc | String | 否 | 标题辅助信息，建议不超过30个字 |
| card_image | Object | 是 | 图片样式 |
| card_image.url | String | 是 | 图片的url |
| card_image.aspect_ratio | Float | 否 | 图片的宽高比，宽高比要小于2.25，大于1.3，不填该参数默认1.3 |
| image_text_area | Object | 否 | 左图右文样式 |
| image_text_area.type | Int | 否 | 左图右文样式区域点击事件，0或不填代表没有点击事件，1 代表跳转url，2 代表跳转小程序 |
| image_text_area.url | String | 否 | 点击跳转的url，image_text_area.type是1时必填 |
| image_text_area.appid | String | 否 | 点击跳转的小程序的appid，必须是与当前应用关联的小程序，image_text_area.type是2时必填 |
| image_text_area.pagepath | String | 否 | 点击跳转的小程序的pagepath，image_text_area.type是2时选填 |
| image_text_area.title | String | 否 | 左图右文样式的标题 |
| image_text_area.desc | String | 否 | 左图右文样式的描述 |
| image_text_area.image_url | String | 是 | 左图右文样式的图片url |
| quote_area | Object | 否 | 引用文献样式，建议不与关键数据共用 |
| quote_area.type | Int | 否 | 引用文献样式区域点击事件，0或不填代表没有点击事件，1 代表跳转url，2 代表跳转小程序 |
| quote_area.url | String | 否 | 点击跳转的url，quote_area.type是1时必填 |
| quote_area.appid | String | 否 | 点击跳转的小程序的appid，quote_area.type是2时必填 |
| quote_area.pagepath | String | 否 | 点击跳转的小程序的pagepath，quote_area.type是2时选填 |
| quote_area.title | String | 否 | 引用文献样式的标题 |
| quote_area.quote_text | String | 否 | 引用文献样式的引用文案 |
| vertical_content_list | Object[] | 否 | 卡片二级垂直内容，该字段可为空数组，但有数据的话需确认对应字段是否必填，列表长度不超过4 |
| vertical_content_list.title | String | 是 | 卡片二级标题，建议不超过26个字 |
| vertical_content_list.desc | String | 否 | 二级普通文本，建议不超过112个字 |
| horizontal_content_list | Object[] | 否 | 二级标题+文本列表，该字段可为空数组，但有数据的话需确认对应字段是否必填，列表长度不超过6 |
| horizontal_content_list.type | Int | 否 | 模版卡片的二级标题信息内容支持的类型，1是url，2是文件附件，3 代表点击跳转成员详情 |
| horizontal_content_list.keyname | String | 是 | 二级标题，建议不超过5个字 |
| horizontal_content_list.value | String | 否 | 二级文本，如果horizontal_content_list.type是2，该字段代表文件名称（要包含文件类型），建议不超过26个字 |
| horizontal_content_list.url | String | 否 | 链接跳转的url，horizontal_content_list.type是1时必填 |
| horizontal_content_list.media_id | String | 否 | 附件的media_id，horizontal_content_list.type是2时必填 |
| horizontal_content_list.userid | String | 否 | 成员详情的userid，horizontal_content_list.type是3时必填 |
| jump_list | Object[] | 否 | 跳转指引样式的列表，该字段可为空数组，但有数据的话需确认对应字段是否必填，列表长度不超过3 |
| jump_list.type | Int | 否 | 跳转链接类型，0或不填代表不是链接，1 代表跳转url，2 代表跳转小程序 |
| jump_list.title | String | 是 | 跳转链接样式的文案内容，建议不超过13个字 |
| jump_list.url | String | 否 | 跳转链接的url，jump_list.type是1时必填 |
| jump_list.appid | String | 否 | 跳转链接的小程序的appid，jump_list.type是2时必填 |
| jump_list.pagepath | String | 否 | 跳转链接的小程序的pagepath，jump_list.type是2时选填 |
| card_action | Object | 是 | 整体卡片的点击跳转事件，news_notice模版卡片中该字段为必填项 |
| card_action.type | Int | 是 | 卡片跳转类型，1 代表跳转url，2 代表打开小程序。news_notice模版卡片中该字段取值范围为[1,2] |
| card_action.url | String | 否 | 跳转事件的url，card_action.type是1时必填 |
| card_action.appid | String | 否 | 跳转事件的小程序的appid，card_action.type是2时必填 |
| card_action.pagepath | String | 否 | 跳转事件的小程序的pagepath，card_action.type是2时选填 |

## 使用示例

### 文本通知模版卡片
```python
# 发送简单的文本通知卡片
await qyweixin_template_card(
    card_type="text_notice",
    main_title_title="系统通知",
    main_title_desc="重要消息提醒",
    sub_title_text="您有新的待处理事项",
    card_action_type=1,
    card_action_url="https://example.com/task"
)

# 发送带有关键数据的文本通知卡片
await qyweixin_template_card(
    card_type="text_notice",
    main_title_title="销售业绩报告",
    emphasis_content_title="156%",
    emphasis_content_desc="完成率",
    horizontal_content_list=[
        {"keyname": "销售额", "value": "100万"},
        {"keyname": "增长率", "value": "25%"}
    ],
    card_action_type=1,
    card_action_url="https://example.com/report"
)
```

### 图文展示模版卡片
```python
# 发送图文展示卡片
await qyweixin_template_card(
    card_type="news_notice",
    main_title_title="产品发布会",
    main_title_desc="新品即将发布",
    card_image_url="https://example.com/product.jpg",
    card_image_aspect_ratio=1.8,
    vertical_content_list=[
        {"title": "创新功能", "desc": "全新用户体验"}
    ],
    card_action_type=1,
    card_action_url="https://example.com/event"
)
```

## 设计要点

### 颜色系统
- **来源文字颜色**：
  - 0：灰色（默认）
  - 1：黑色
  - 2：红色
  - 3：绿色

### 字符长度建议
- 来源描述：≤13个字
- 一级标题：≤26个字
- 标题辅助信息：≤30个字
- 关键数据内容：≤10个字
- 关键数据描述：≤15个字
- 二级普通文本：≤112个字
- 二级标题：≤5个字
- 二级文本：≤26个字
- 跳转链接文案：≤13个字

### 数组长度限制
- horizontal_content_list：≤6个
- jump_list：≤3个
- vertical_content_list：≤4个（仅news_notice）

### 图片规范
- **card_image 宽高比**：1.3 ≤ aspect_ratio ≤ 2.25
- **推荐比例**：1.8（16:9）
- **图片格式**：JPG、PNG
- **图片大小**：建议压缩后使用

## 最佳实践

1. **内容层次分明**：合理使用一级标题、二级标题、普通文本
2. **关键信息突出**：text_notice使用emphasis_content展示重要数据
3. **图文搭配**：news_notice充分利用图片增强视觉效果
4. **交互设计**：合理设置跳转链接和点击事件
5. **信息密度**：避免信息过载，保持内容简洁明了

## 常见问题

### Q: 文本通知和图文展示应该如何选择？
A: 文本通知适合数据展示、系统通知；图文展示适合产品推广、活动宣传。

### Q: 图片宽高比有什么要求？
A: news_notice中card_image的aspect_ratio必须在1.3-2.25之间，推荐使用1.8。

### Q: 可以设置多少个跳转按钮？
A: jump_list最多支持3个跳转按钮，horizontal_content_list最多支持6个。

### Q: 如何处理小程序跳转？
A: 设置type=2，并提供appid，pagepath为可选参数。

## 错误处理

- 缺少必填字段会返回参数错误
- 图片链接无效不会报错但图片不显示
- 宽高比超出范围会使用默认值1.3
- 文本长度超出建议值会被截断
- 数组长度超出限制会被忽略

## 注意事项

1. card_action为必填字段，决定整个卡片的点击行为
2. text_notice的main_title.title和sub_title_text至少填写一个
3. news_notice的main_title.title和card_image.url为必填字段
4. 引用文献样式建议不与关键数据共用
5. 小程序跳转需要确保appid与当前应用关联
6. 模版卡片在不同企业微信版本中显示效果可能略有差异 