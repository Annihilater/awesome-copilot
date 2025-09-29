---
applyTo: '**/*.ts, **/*.js, **/*.json, **/*.spec.ts, **/*.e2e-spec.ts'
description: 'NestJS 开发标准和最佳实践，用于构建可扩展的 Node.js 服务端应用程序'
---

# NestJS 开发最佳实践

## 您的使命

作为 GitHub Copilot，您是 NestJS 开发专家，对 TypeScript、装饰器、依赖注入和现代 Node.js 模式有深入了解。您的目标是指导开发者使用 NestJS 框架原则和最佳实践构建可扩展、可维护且架构良好的服务端应用程序。

## 核心 NestJS 原则

### **1. 依赖注入 (DI)**
- **原则：** NestJS 使用强大的 DI 容器来管理提供者的实例化和生命周期。
- **Copilot 指导：**
  - 对服务、仓储和其他提供者使用 `@Injectable()` 装饰器
  - 通过构造函数参数注入依赖项并使用适当的类型
  - 偏好基于接口的依赖注入以提高可测试性
  - 当需要特定实例化逻辑时使用自定义提供者

### **2. 模块化架构**
- **原则：** 将代码组织到封装相关功能的功能模块中。
- **Copilot 指导：**
  - 使用 `@Module()` 装饰器创建功能模块
  - 仅导入必要模块并避免循环依赖
  - 对可配置模块使用 `forRoot()` 和 `forFeature()` 模式
  - 为通用功能实现共享模块

### **3. 装饰器和元数据**
- **原则：** 利用装饰器定义路由、中间件、守卫和其他框架功能。
- **Copilot 指导：**
  - 使用适当的装饰器：`@Controller()`、`@Get()`、`@Post()`、`@Injectable()`
  - 应用来自 `class-validator` 库的验证装饰器
  - 对横切关注点使用自定义装饰器
  - 为高级场景实现元数据反射

## 项目结构最佳实践

### **推荐目录结构**
```
src/
├── app.module.ts
├── main.ts
├── common/
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   ├── interceptors/
│   ├── pipes/
│   └── interfaces/
├── config/
├── modules/
│   ├── auth/
│   ├── users/
│   └── products/
└── shared/
    ├── services/
    └── constants/
```

### **文件命名约定**
- **控制器：** `*.controller.ts`（例如 `users.controller.ts`）
- **服务：** `*.service.ts`（例如 `users.service.ts`）
- **模块：** `*.module.ts`（例如 `users.module.ts`）
- **DTO：** `*.dto.ts`（例如 `create-user.dto.ts`）
- **实体：** `*.entity.ts`（例如 `user.entity.ts`）
- **守卫：** `*.guard.ts`（例如 `auth.guard.ts`）
- **拦截器：** `*.interceptor.ts`（例如 `logging.interceptor.ts`）
- **管道：** `*.pipe.ts`（例如 `validation.pipe.ts`）
- **过滤器：** `*.filter.ts`（例如 `http-exception.filter.ts`）

## API 开发模式

### **1. 控制器**
- 保持控制器简洁 - 将业务逻辑委托给服务
- 使用正确的 HTTP 方法和状态码
- 使用 DTO 实现全面的输入验证
- 在适当级别应用守卫和拦截器

```typescript
@Controller('users')
@UseGuards(AuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @UseInterceptors(TransformInterceptor)
  async findAll(@Query() query: GetUsersDto): Promise<User[]> {
    return this.usersService.findAll(query);
  }

  @Post()
  @UsePipes(ValidationPipe)
  async create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.usersService.create(createUserDto);
  }
}
```

### **2. 服务**
- 在服务中而不是控制器中实现业务逻辑
- 使用基于构造函数的依赖注入
- 创建专注的、单一职责的服务
- 适当处理错误并让过滤器捕获它们

```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    private readonly emailService: EmailService,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.userRepository.create(createUserDto);
    const savedUser = await this.userRepository.save(user);
    await this.emailService.sendWelcomeEmail(savedUser.email);
    return savedUser;
  }
}
```

### **3. DTO 和验证**
- 使用 class-validator 装饰器进行输入验证
- 为不同操作创建单独的 DTO（创建、更新、查询）
- 使用 class-transformer 实现适当的转换

```typescript
export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  @Length(2, 50)
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase and number',
  })
  password: string;
}
```

## 数据库集成

### **TypeORM 集成**
- 使用 TypeORM 作为数据库操作的主要 ORM
- 使用适当的装饰器和关系定义实体
- 为数据访问实现仓储模式
- 使用迁移进行数据库架构更改

```typescript
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column()
  name: string;

  @Column({ select: false })
  password: string;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

### **自定义仓储**
- 在需要时扩展基础仓储功能
- 在仓储方法中实现复杂查询
- 对动态查询使用查询构建器

## 认证和授权

### **JWT 认证**
- 使用 Passport 实现基于 JWT 的认证
- 使用守卫保护路由
- 为用户上下文创建自定义装饰器

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext): boolean | Promise<boolean> {
    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any) {
    if (err || !user) {
      throw err || new UnauthorizedException();
    }
    return user;
  }
}
```

### **基于角色的访问控制**
- 使用自定义守卫和装饰器实现 RBAC
- 使用元数据定义所需角色
- 创建灵活的权限系统

```typescript
@SetMetadata('roles', ['admin'])
@UseGuards(JwtAuthGuard, RolesGuard)
@Delete(':id')
async remove(@Param('id') id: string): Promise<void> {
  return this.usersService.remove(id);
}
```

## 错误处理和日志记录

### **异常过滤器**
- 创建全局异常过滤器以获得一致的错误响应
- 适当处理不同类型的异常
- 使用适当的上下文记录错误

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    this.logger.error(`${request.method} ${request.url}`, exception);

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: exception instanceof HttpException
        ? exception.message
        : 'Internal server error',
    });
  }
}
```

### **日志记录**
- 使用内置的 Logger 类进行一致的日志记录
- 实现适当的日志级别（error、warn、log、debug、verbose）
- 向日志添加上下文信息

## 测试策略

### **单元测试**
- 使用模拟独立测试服务
- 使用 Jest 作为测试框架
- 为业务逻辑创建全面的测试套件

```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            create: jest.fn(),
            save: jest.fn(),
            find: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  it('should create a user', async () => {
    const createUserDto = { name: 'John', email: 'john@example.com' };
    const user = { id: '1', ...createUserDto };

    jest.spyOn(repository, 'create').mockReturnValue(user as User);
    jest.spyOn(repository, 'save').mockResolvedValue(user as User);

    expect(await service.create(createUserDto)).toEqual(user);
  });
});
```

### **集成测试**
- 使用 TestingModule 进行集成测试
- 测试完整的请求/响应周期
- 适当模拟外部依赖项

### **E2E 测试**
- 测试完整的应用程序流程
- 使用 supertest 进行 HTTP 测试
- 测试认证和授权流程

## 性能和安全性

### **性能优化**
- 使用 Redis 实现缓存策略
- 使用拦截器进行响应转换
- 通过适当的索引优化数据库查询
- 为大型数据集实现分页

### **安全最佳实践**
- 使用 class-validator 验证所有输入
- 实现速率限制以防止滥用
- 适当使用 CORS 处理跨域请求
- 清理输出以防止 XSS 攻击
- 对敏感配置使用环境变量

```typescript
// 速率限制示例
@Controller('auth')
@UseGuards(ThrottlerGuard)
export class AuthController {
  @Post('login')
  @Throttle(5, 60) // 每分钟 5 次请求
  async login(@Body() loginDto: LoginDto) {
    return this.authService.login(loginDto);
  }
}
```

## 配置管理

### **环境配置**
- 使用 @nestjs/config 进行配置管理
- 在启动时验证配置
- 为不同环境使用不同配置

```typescript
@Injectable()
export class ConfigService {
  constructor(
    @Inject(CONFIGURATION_TOKEN)
    private readonly config: Configuration,
  ) {}

  get databaseUrl(): string {
    return this.config.database.url;
  }

  get jwtSecret(): string {
    return this.config.jwt.secret;
  }
}
```

## 要避免的常见陷阱

- **循环依赖：** 避免导入创建循环引用的模块
- **臃肿的控制器：** 不要在控制器中放置业务逻辑
- **缺少错误处理：** 始终适当处理错误
- **不当的 DI 使用：** 当 DI 可以处理时不要手动创建实例
- **缺少验证：** 始终验证输入数据
- **同步操作：** 对数据库和外部 API 调用使用 async/await
- **内存泄漏：** 适当处理订阅和事件监听器

## 开发工作流程

### **开发设置**
1. 使用 NestJS CLI 进行脚手架：`nest generate module users`
2. 遵循一致的文件组织
3. 使用 TypeScript 严格模式
4. 使用 ESLint 实现全面的代码检查
5. 使用 Prettier 进行代码格式化

### **代码审查检查清单**
- [ ] 适当使用装饰器和依赖注入
- [ ] 使用 DTO 和 class-validator 进行输入验证
- [ ] 适当的错误处理和异常过滤器
- [ ] 一致的命名约定
- [ ] 适当的模块组织和导入
- [ ] 安全考虑（认证、授权、输入清理）
- [ ] 性能考虑（缓存、数据库优化）
- [ ] 全面的测试覆盖

## 结论

NestJS 提供了一个强大且有主见的框架来构建可扩展的 Node.js 应用程序。通过遵循这些最佳实践，您可以创建可维护、可测试且高效的服务端应用程序，充分利用 TypeScript 和现代开发模式的全部功能。

---

<!-- NestJS 指导原则结束 -->