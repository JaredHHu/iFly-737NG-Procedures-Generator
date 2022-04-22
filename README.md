# iFly-737NG-Procedures-Generator
iFly 737NG for P3D V5 导航数据生成器

## 对于版本号的编排规则
项目采用**客制化的语义化版本号系统**，格式如下：
``` Text
{Major}.{Minor}.{Reversion}.{Build}
```

其中`Major`为主要版本号，有重要功能性更新时自增1；`Minor`为次要版本号，有次要功能性更新时自增1，`Major`更新时归零；`Reversion`为修订号，指当前次要版本号第一次发布以来经历的修复性更新的次数，`Minor`更新时归零；`Build`为构建号，为从第一个发行版本后第几次构建，原则上每次以`Release`配置生成工程时都应增1，且**从不归零**。
