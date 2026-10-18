# SHANXING — PVC Shoe Charms Factory Landing

B2B 独立站,用 SEO 内容给福建 PVC 鞋花工厂获取海外买家询盘。
打法复制自 [antigravity-proxy-landing](https://github.com/Arismemo/antigravity-proxy-landing) 的成功模式:结构化长内容 + Schema 富媒体 + 全渠道 CTA 漏斗。

## 站点结构

```
├── index.html      首页(落地页 + 4 重 Schema + 全渠道 CTA)
├── guide.html      采购指南长内容(HowTo 七步 + 长尾 SEO 主力)
├── 404.html        自定义 404
├── robots.txt      全开放
├── sitemap.xml     含 2 个 URL
├── scripts/validate_site.py 静态回归测试（Schema/链接/文案/WhatsApp来源）
├── favicon.svg     站点图标
└── SEO_STRATEGY.md 完整 SEO 方案文档
```

## 本地预览

```bash
cd /Users/liukun/j/factory_web
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

## 部署到 GitHub Pages

```bash
# 1. 创建远程仓库(名:pvc-shoe-charms-factory)
gh repo create Arismemo/pvc-shoe-charms-factory --public

# 2. 初始化并推送
git init && git add . && git commit -m "init: SHANXING PVC shoe charms factory site"
git branch -M main
git remote add origin https://github.com/Arismemo/pvc-shoe-charms-factory.git
git push -u origin main

# 3. 开启 GitHub Pages(main 分支根目录)
gh api -X POST repos/Arismemo/pvc-shoe-charms-factory/pages \
  -f "source[branch]=main" -f "source[path]=/"
```

部署后访问: https://arismemo.github.io/pvc-shoe-charms-factory/

## 关键 SEO 配置(已植入)

| 项目 | 首页 | 指南页 |
|---|---|---|
| Organization/Manufacturer | ✅ | — |
| Product (AggregateOffer) | ✅ | — |
| FAQPage | ✅ 6 题 | ✅ 5 题 |
| HowTo (7 步) | — | ✅ |
| TechArticle | — | ✅ |
| BreadcrumbList | ✅ | — |
| Open Graph / Twitter | ✅ | ✅ |
| canonical | ✅ | ✅ |
| sitemap + robots | ✅ | ✅ |

## 2026-08-09 转化与事实修订

- 报价改为“先给 budgetary answer，再按 artwork/物流复核 final quote”
- WhatsApp CTA 与表单自动带 `Source: SHANXING website`，可识别网站线索
- 明确“模具制造委外、鞋花产品生产在本厂”
- 材料检测仅按供应商报告覆盖范围表述，不扩大成所有成品/批次认证（2026-10-18 工厂拿不出供应商检测报告原件，改为不提供报告，只写可安排有资质的第三方实验室检测产前样，费用另报）
- 去除无依据的市场规模、绝对领先、固定物流与免费样品等承诺（2026-10-18 改为现货样品免费、运费客户付，见工作区 决策记录.md）
- 加入 IP、品牌非关联、进口与检测边界

## 待补素材(影响转化,不影响上线)

- [ ] 产品图片 / 设计稿(放 images/ 目录)
- [ ] 工厂实景 / 车间照片
- [ ] 认证证书扫描件(EN71/CPSIA)
- [ ] og_image.webp(1200×630 分享图)
- [ ] 真实案例图(已出货的鞋花成品照)

## 发布前验证

```bash
python3 scripts/validate_site.py
python3 -m http.server 8000
```

## 上线后必做

1. [Google Search Console](https://search.google.com/search-console) 添加站点,提交 sitemap.xml
2. 等 3-7 天收录后,监控"performance"报告看实际触发词
3. 根据搜索词报告迭代 guide.html 内容
4. 后续可绑自有域名(在 repo Settings → Pages → Custom domain)
