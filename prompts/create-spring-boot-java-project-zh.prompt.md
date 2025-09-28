---
mode: "agent"
description: "创建 Spring Boot Java 项目骨架"
---

# 创建 Spring Boot Java 项目提示

- 请确保您的系统上安装了以下软件：

  - Java 21
  - Docker
  - Docker Compose

- 如果您需要自定义项目名称，请在 [下载 Spring Boot 项目模板](./create-spring-boot-java-project-zh.prompt.md#download-spring-boot-project-template) 中更改 `artifactId` 和 `packageName`

- 如果您需要更新 Spring Boot 版本，请在 [下载 Spring Boot 项目模板](./create-spring-boot-java-project-zh.prompt.md#download-spring-boot-project-template) 中更改 `bootVersion`

## 检查 Java 版本

- 在终端中运行以下命令并检查 Java 版本

```shell
java -version
```

## 下载 Spring Boot 项目模板

- 在终端中运行以下命令以下载 Spring Boot 项目模板

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-java} \
  -d bootVersion=3.4.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

## 解压下载的文件

- 在终端中运行以下命令以解压下载的文件

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
```

## 删除下载的 zip 文件

- 在终端中运行以下命令以删除下载的 zip 文件

```shell
rm -f starter.zip
```

## 将目录更改为项目根目录

- 在终端中运行以下命令以将目录更改为项目根目录

```shell
cd ${input:projectName:demo-java}
```

## 添加其他依赖项

- 将 `springdoc-openapi-starter-webmvc-ui` 和 `archunit-junit5` 依赖项插入 `pom.xml` 文件

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

## 添加 SpringDoc、Redis、JPA 和 MongoDB 配置

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

- 将 JPA 配置插入 `application.properties` 文件

```properties
# JPA 配置
spring.jpa.hibernate.ddl-auto=none
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
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
./mvnw spring-boot:run
```
