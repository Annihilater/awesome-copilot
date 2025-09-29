---
description: 'C++ 项目配置和包管理'
applyTo: '**/*.cmake, **/CMakeLists.txt, **/*.cpp, **/*.h, **/*.hpp'
---

此项目使用 vcpkg 的 manifest 模式。在提供 vcpkg 建议时请记住这一点。不要提供像 vcpkg install library 这样的建议，因为它们不会按预期工作。
如果可能的话，优先通过 CMakePresets.json 设置缓存变量和其他类型的配置。
提供关于可能影响所建议或提及的 CMake 变量的任何 CMake 策略的信息。
此项目需要跨平台和跨编译器兼容，支持 MSVC、Clang 和 GCC。
在提供使用文件系统读取文件的 OpenCV 示例时，请始终使用绝对文件路径而不是文件名或相对文件路径。例如，使用 `video.open("C:/project/file.mp4")`，而不是 `video.open("file.mp4")`。