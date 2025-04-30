# 🛠️ My Everyday CLI Tools  

Welcome to my collection of handy CLI tools built to automate and simplify repetitive tasks. If you find yourself dealing with similar routines, feel free to try them out—they might save you some keystrokes!  

---

## 📦 Overview  

This repo contains a growing set of lightweight, hackable command-line utilities written in Python. They’re designed to streamline common tasks and make terminal workflows easier.  

---

## 🚀 Getting Started  

The tools include pre-built `exe` files in the `dist` folder (primarily for Windows—WSL works for Linux needs). You can:  
- Clone the repo, or  
- Download the binary and add it to your `PATH` for global access.  

---

## 🛠️ Tools  

### **`frid`**  
A CLI tool to launch an Android Virtual Device (AVD) by name (only those set up via Android Studio) and start the Frida server on it (saved as `frida-server` on the emulator).  

#### **Prerequisites**  
- **Android Studio**: Installed with at least one AVD configured.  
- **Frida**: The `frida-server` binary must be available on the emulator.  
- **Emulator Path**: Ensure `emulator.exe` is in your system’s `PATH` (default: `C:\Users\<Username>\AppData\Local\Android\Sdk\emulator`).  

#### **Usage**  
```bash
frid <avd_name>
```

---

### **`buildqbdi`**  
Automates the setup of the Visual Studio environment and compiles C++ files using the QBDI library.  

#### **Prerequisites**  
1. **Visual Studio Build Tools**  
   - Install **Desktop development with C++** (includes `cl.exe`).  
   - Download: [Visual Studio](https://visualstudio.microsoft.com/downloads/).  

2. **QBDI Library**  
   - Precompiled binaries or source from [QBDI GitHub](https://github.com/QBDI/QBDI).  
   - Ensure include/lib paths are accessible.  

#### **Usage**  
```bash
buildqbdi <path_to_your_cpp_file>
```

---

## 🔧 Notes  
- For Linux/WSL support, contributions are welcome!  
- Tools are designed for simplicity—modify as needed for your workflow.  