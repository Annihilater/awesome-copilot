---
mode: "agent"
description: "创建 Spring Boot Kotlin 项目骨架"
---

# 创建 Spring Boot Kotlin 项目提示

- 请确保您的系统上安装了以下软件：

  - Java 21
  - Docker
  - Docker Compose

- 如果您需要自定义项目名称，请在 [下载 Spring Boot 项目模板](./create-spring-boot-kotlin-project-zh.prompt.md#download-spring-boot-project-template) 中更改 `artifactId` 和 `packageName`

- 如果您需要更新 Spring Boot 版本，请在 [下载 Spring Boot 项目模板](./create-spring-boot-kotlin-project-zh.prompt.md#download-spring-boot-project-template) 中更改 `bootVersion`

## 检查 Java 版本

- 在终端中运行以下命令并检查 Java 版本

```shell
java -version
```

## 下载 Spring Boot 项目模板

- 在终端中运行以下命令以下载 Spring Boot 项目模板

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-kotlin} \
  -d bootVersion=3.4.5 \
  -d dependencies=configuration-processor,webflux,data-r2dbc,postgresql,data-redis-reactive,data-mongodb-reactive,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d language=kotlin \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=gradle-project-kotlin \
  -o starter.zip
```

## 解压下载的文件

- 在终端中运行以下命令以解压下载的文件

```shell
unzip starter.zip -d ./${input:projectName:demo-kotlin}
```

## 删除下载的 zip 文件

- 在终端中运行以下命令以删除下载的 zip 文件

```shell
rm -f starter.zip
```

## 将目录更改为项目根目录

- 在终端中运行以下命令以将目录更改为项目根目录

```shell
cd ${input:projectName:demo-kotlin}
```

## 添加其他依赖项

- 将 `springdoc-openapi-starter-webmvc-ui` 和 `archunit-junit5` 依赖项插入 `build.gradle.kts` 文件

```gradle.kts
dependencies {
  implementation("org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.6")
  testImplementation("com.tngtech.archunit:archunit-junit5:1.2.1")
}
```

## 添加 SpringDoc、Redis、R2DBC 和 MongoDB 配置

- 将 SpringDoc 配置插入 `application.properties` 文件

```properties
# SpringDoc 配置
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

- 将 Redis 配置插入 `application.properties` 文件

```properties
# Redis 配置
spring.data.redis.host=localhost
spring.data.redis.port=6379
```

- 将 R2DBC 配置插入 `application.properties` 文件

```properties
# R2DBC 配置
spring.r2dbc.url=r2dbc:postgresql://localhost:5432/postgres
spring.r2dbc.username=user
spring.r2dbc.password=password
```

- 将 MongoDB 配置插入 `application.properties` 文件

```properties
# MongoDB 配置
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
```

## 添加 Docker Compose 文件

- 在项目根目录中创建一个 `compose.yaml` 文件

```yaml
services:
  postgres:
    image: postgres:16.4-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=db
  redis:
    image: redis:7.2.5-alpine
    container_name: redis
    ports:
      - "6379:6379"
  mongo:
    image: mongo:7.0.12
    container_name: mongo
    ports:
      - "27017:27017"
```

## 启动 Docker 容器

- 在终端中运行以下命令以启动 Docker 容器

```shell
docker compose up -d
```

## 运行应用程序

- 在终端中运行以下命令以运行应用程序

```shell
./gradlew bootRun
```
