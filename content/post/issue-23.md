---
title: "利用GitHub Actions拯救MatterMost安卓客户端坑爹的消息推送"
date: "2020-07-13T15:37:46+08:00"
tags: ['Idea', 'Linux', 'Python']
comments: false
---

> created_date: 2020-07-13T15:37:46+08:00

> update_date: 2020-07-13T15:38:08+08:00

> comment_url: https://github.com/ferstar/blog/issues/23

MatterMost是一款非常好用的团队沟通工具，但是这货的安卓客户端推送服务非常的佛系，夸张到昨天的消息今天才可能收到，有时候团队有啥要紧事的时候就很蛋疼，只能在微信群里at某某某，体验很不好。所幸他的API非常详细，通过一番组合加上GitHub Actions服务完全可以拯救糟糕的消息推送。

### 1. 利用到的服务

- AlertOver: https://www.alertover.com
- GitHub Actions: https://github.com/features/actions

### 2. 用到的API

> 就是遍历所有频道，拿到未读消息计数，利用AlertOver进行推送

1. 公开频道未读消息 `/api/v4/users/me/teams/unread`
2. 列出所有频道 `/api/v4/users/me/teams/<channel_id>/channels`
3. 列出频道未读消息 `/api/v4/users/me/channels/<channel_id>/unread`
4. 推送AlertOver `https://api.alertover.com/v1/alert`

### 3. 配置AlertOver服务&安装客户端

> 这个没啥好说的，注册账号，下载安装客户端，比较开心的是，客户端支持 MIPush，不用单独给他留后台服务。然后再新建一个组织，如图
![image](https://user-images.githubusercontent.com/2854276/87322778-6b8a9d00-c560-11ea-9e7b-180247f5c0a5.png)

### 4. 配置GitHub Actions

1. 代码部分：https://github.com/ferstar/blog/blob/master/static/mm_notify.py
2. workflow：https://github.com/ferstar/blog/blob/master/.github/workflows/mm_notify.yml
3. secrets配置：敏感信息，如cookie等可以配置到这里，如图
![image](https://user-images.githubusercontent.com/2854276/87323301-2e72da80-c561-11ea-95a0-895f81144984.png)

### 5. 最终效果

> 一番折腾后，手机上可以比较及时的收到MatterMost中的未读消息提示，飒！

![image](https://user-images.githubusercontent.com/2854276/87323600-93c6cb80-c561-11ea-8fc2-fc8c0a0bc730.png)

