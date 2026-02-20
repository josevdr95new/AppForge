# AppForge - Capacitor APK Builder

[![Build Android App](https://github.com/josevdr95new/AppForge/actions/workflows/build.yml/badge.svg)](https://github.com/josevdr95new/AppForge/actions/workflows/build.yml)

**[🇪🇸 Español](#español)** | **[🇬🇧 English](#english)**

---

## Español <a name="español"></a>

### 📱 Descripción

**AppForge** es una plantilla para crear aplicaciones Android (APK) a partir de aplicaciones web (HTML/CSS/JS) usando **Capacitor** y GitHub Actions. Compilación automática en la nube.

### ✨ Características

- 🔄 **Compilación automática** - Compila APK en GitHub Actions con keywords
- 📱 **APK Debug listo** - El APK generado es instalable directamente
- ⚙️ **Configuración centralizada** - Todo en `app.config.json`
- 🎨 **Assets autogenerados** - Iconos y splash desde un solo archivo fuente
- 🤖 **Pruebas en emulador** - Capturas automáticas en GitHub Actions
- 🔗 **Deep Links** - URLs personalizadas para abrir tu app
- 🖥️ **Editor visual** - Configuración gráfica con Python

### 📁 Estructura del Proyecto

```
AppForge/
├── .github/workflows/
│   └── build.yml              # Workflow de GitHub Actions
├── assets/                    # Iconos y splash
│   ├── icon.png               # Icono (1024x1024 mínimo)
│   ├── splash.png             # Splash (2732x2732 mínimo)
│   └── splash-dark.png        # Splash oscuro (opcional)
├── www/                       # Archivos web
│   ├── index.html             # Página principal
│   ├── css/style.css          # Estilos
│   └── js/app.js              # JavaScript
├── app.config.json            # Configuración ⭐
├── config_editor.py           # Editor visual
├── capacitor.config.json      # Configuración Capacitor
└── package.json               # Dependencias
```

### 🚀 Inicio Rápido

#### 1. Clonar el repositorio

```bash
git clone https://github.com/josevdr95new/AppForge.git
cd AppForge
```

#### 2. Configurar la aplicación

Usa el editor visual o edita `app.config.json`:

```bash
python config_editor.py
```

O manualmente:

```json
{
  "appId": "com.tuempresa.tuapp",
  "appName": "Tu App",
  "version": "1.0.0",
  "versionCode": 1,
  "android": {
    "minSdkVersion": 24,
    "targetSdkVersion": 34,
    "permissions": ["android.permission.INTERNET"]
  },
  "deepLinks": {
    "enabled": false,
    "scheme": "miapp",
    "host": "miapp.com",
    "paths": ["/producto/:id", "/usuario/:username"]
  },
  "build": {
    "compile": true,
    "emulator": false
  }
}
```

#### 3. Añadir archivos web

Coloca tus archivos en `www/`:

```
www/
├── index.html      ← Obligatorio
├── css/style.css
└── js/app.js
```

#### 4. Añadir icono y splash

Crea la carpeta `assets/`:

```
assets/
├── icon.png        # 1024x1024 mínimo - REQUERIDO
└── splash.png      # 2732x2732 mínimo - OPCIONAL
```

#### 5. Compilar

```bash
git add .
git commit -m "Mi app lista [compile]"
git push origin main
```

### 📥 Descargar el APK

1. Ve a **Actions** en GitHub
2. Selecciona el workflow completado
3. Descarga **App-Instalable**
4. El archivo `Tu-App-v1.0.0.apk` está listo

### ⚙️ Control de Compilación

| Keyword | Acción |
|---------|--------|
| `[compile]` `[compilar]` `[build]` | Compila |
| `[skip]` `[noc]` | No compila |
| Sin keyword | Depende de `build.compile` |

### 📋 app.config.json - Referencia Completa

| Campo | Descripción | Default |
|-------|-------------|---------|
| `appId` | ID único (ej: com.empresa.app) | - |
| `appName` | Nombre visible | - |
| `version` | Versión semántica (x.x.x) | 1.0.0 |
| `versionCode` | Número de build | 1 |
| `android.minSdkVersion` | SDK mínimo | 24 |
| `android.targetSdkVersion` | SDK objetivo | 34 |
| `android.permissions` | Array de permisos | [] |
| `deepLinks.enabled` | Habilitar deep links | false |
| `deepLinks.scheme` | Esquema URL (ej: miapp) | - |
| `deepLinks.host` | Dominio App Links | - |
| `deepLinks.paths` | Rutas soportadas | [] |
| `build.compile` | Compilar automáticamente | true |
| `build.emulator` | Ejecutar emulador + capturas | false |

### 🤖 Pruebas con Emulador

Con `"emulator": true`:

1. Inicia emulador Android
2. Instala el APK
3. Espera 30s → captura 1
4. Espera 30s → captura 2
5. Espera 30s → captura 3
6. Sube artifact **Emulator-Screenshots**

**Nota:** +10-15 min de build time.

### 🔗 Deep Links

```json
{
  "deepLinks": {
    "enabled": true,
    "scheme": "miapp",
    "host": "miapp.com",
    "paths": ["/producto/:id", "/usuario/:username"]
  }
}
```

**Ejemplos:**

```bash
miapp://producto/123
miapp://usuario/juan?ref=email
https://miapp.com/promo/VERANO2025
```

**Probar:**

```bash
adb shell am start -a android.intent.action.VIEW -d "miapp://test"
```

### 🖥️ Editor Visual

```bash
python config_editor.py
```

Editor gráfico con:
- Pestañas: General, Permisos, Build, Deep Links
- Permisos predefinidos + personalizados
- Paths de deep links múltiples
- Incrementar versión con un clic

### 🔌 Plugins Incluidos

| Plugin | Uso |
|--------|-----|
| `@capacitor/app` | Estado de la app |
| `@capacitor/browser` | Enlaces externos |
| `@capacitor/camera` | Cámara |
| `@capacitor/geolocation` | GPS |
| `@capacitor/network` | Estado de red |
| `@capacitor/preferences` | Almacenamiento |
| `@capacitor/splash-screen` | Pantalla de carga |
| `@capacitor/status-bar` | Barra de estado |
| `@capacitor/toast` | Notificaciones |

### 💻 API Disponible

```javascript
// Cámara
const photo = await takePhoto();
const image = await pickImage();

// Ubicación
const location = await getLocation();

// Red
const status = await getNetworkStatus();

// Almacenamiento
await saveData('key', data);
const data = await loadData('key');

// Toast
await showToast('Mensaje');

// Enlaces externos
openExternalLink('https://google.com');

// Deep Links (automático)
// miapp://producto/123 → action: 'view_product', data: { productId: '123' }
```

### 🛠️ Desarrollo Local

```bash
npm install
npx cap add android
npx cap sync
npx cap open android    # Abre Android Studio
npx cap run android     # Ejecuta en dispositivo
```

---

## English <a name="english"></a>

### 📱 Description

**AppForge** is a template to create Android apps (APK) from web applications (HTML/CSS/JS) using **Capacitor** and GitHub Actions. Automatic cloud compilation.

### ✨ Features

- 🔄 **Automatic compilation** - APK builds in GitHub Actions with keywords
- 📱 **Debug APK ready** - Generated APK is directly installable
- ⚙️ **Centralized configuration** - Everything in `app.config.json`
- 🎨 **Auto-generated assets** - Icons and splash from single source
- 🤖 **Emulator testing** - Automatic screenshots in GitHub Actions
- 🔗 **Deep Links** - Custom URLs to open your app
- 🖥️ **Visual editor** - Graphical configuration with Python

### 📁 Project Structure

```
AppForge/
├── .github/workflows/
│   └── build.yml              # GitHub Actions workflow
├── assets/                    # Icons and splash
│   ├── icon.png               # Icon (1024x1024 min)
│   ├── splash.png             # Splash (2732x2732 min)
│   └── splash-dark.png        # Dark splash (optional)
├── www/                       # Web files
│   ├── index.html             # Main page
│   ├── css/style.css          # Styles
│   └── js/app.js              # JavaScript
├── app.config.json            # Configuration ⭐
├── config_editor.py           # Visual editor
├── capacitor.config.json      # Capacitor config
└── package.json               # Dependencies
```

### 🚀 Quick Start

#### 1. Clone the repository

```bash
git clone https://github.com/josevdr95new/AppForge.git
cd AppForge
```

#### 2. Configure the application

Use the visual editor or edit `app.config.json`:

```bash
python config_editor.py
```

Or manually:

```json
{
  "appId": "com.yourcompany.yourapp",
  "appName": "Your App",
  "version": "1.0.0",
  "versionCode": 1,
  "android": {
    "minSdkVersion": 24,
    "targetSdkVersion": 34,
    "permissions": ["android.permission.INTERNET"]
  },
  "deepLinks": {
    "enabled": false,
    "scheme": "myapp",
    "host": "myapp.com",
    "paths": ["/product/:id", "/user/:username"]
  },
  "build": {
    "compile": true,
    "emulator": false
  }
}
```

#### 3. Add web files

Place your files in `www/`:

```
www/
├── index.html      ← Required
├── css/style.css
└── js/app.js
```

#### 4. Add icon and splash

Create the `assets/` folder:

```
assets/
├── icon.png        # 1024x1024 min - REQUIRED
└── splash.png      # 2732x2732 min - OPTIONAL
```

#### 5. Compile

```bash
git add .
git commit -m "My app ready [compile]"
git push origin main
```

### 📥 Download the APK

1. Go to **Actions** on GitHub
2. Select the completed workflow
3. Download **App-Instalable**
4. The `Your-App-v1.0.0.apk` file is ready

### ⚙️ Build Control

| Keyword | Action |
|---------|--------|
| `[compile]` `[build]` | Compiles |
| `[skip]` `[noc]` | Skips |
| No keyword | Depends on `build.compile` |

### 📋 app.config.json - Full Reference

| Field | Description | Default |
|-------|-------------|---------|
| `appId` | Unique ID (e.g. com.company.app) | - |
| `appName` | Visible name | - |
| `version` | Semantic version (x.x.x) | 1.0.0 |
| `versionCode` | Build number | 1 |
| `android.minSdkVersion` | Min SDK | 24 |
| `android.targetSdkVersion` | Target SDK | 34 |
| `android.permissions` | Permissions array | [] |
| `deepLinks.enabled` | Enable deep links | false |
| `deepLinks.scheme` | URL scheme (e.g. myapp) | - |
| `deepLinks.host` | App Links domain | - |
| `deepLinks.paths` | Supported paths | [] |
| `build.compile` | Auto-compile | true |
| `build.emulator` | Run emulator + screenshots | false |

### 🤖 Emulator Testing

With `"emulator": true`:

1. Starts Android emulator
2. Installs the APK
3. Waits 30s → screenshot 1
4. Waits 30s → screenshot 2
5. Waits 30s → screenshot 3
6. Uploads **Emulator-Screenshots** artifact

**Note:** +10-15 min build time.

### 🔗 Deep Links

```json
{
  "deepLinks": {
    "enabled": true,
    "scheme": "myapp",
    "host": "myapp.com",
    "paths": ["/product/:id", "/user/:username"]
  }
}
```

**Examples:**

```bash
myapp://product/123
myapp://user/john?ref=email
https://myapp.com/promo/SUMMER2025
```

**Test:**

```bash
adb shell am start -a android.intent.action.VIEW -d "myapp://test"
```

### 🖥️ Visual Editor

```bash
python config_editor.py
```

Graphical editor with:
- Tabs: General, Permissions, Build, Deep Links
- Predefined + custom permissions
- Multiple deep link paths
- One-click version increment

### 🔌 Included Plugins

| Plugin | Use |
|--------|-----|
| `@capacitor/app` | App state |
| `@capacitor/browser` | External links |
| `@capacitor/camera` | Camera |
| `@capacitor/geolocation` | GPS |
| `@capacitor/network` | Network status |
| `@capacitor/preferences` | Storage |
| `@capacitor/splash-screen` | Splash screen |
| `@capacitor/status-bar` | Status bar |
| `@capacitor/toast` | Notifications |

### 💻 Available API

```javascript
// Camera
const photo = await takePhoto();
const image = await pickImage();

// Location
const location = await getLocation();

// Network
const status = await getNetworkStatus();

// Storage
await saveData('key', data);
const data = await loadData('key');

// Toast
await showToast('Message');

// External links
openExternalLink('https://google.com');

// Deep Links (automatic)
// myapp://product/123 → action: 'view_product', data: { productId: '123' }
```

### 🛠️ Local Development

```bash
npm install
npx cap add android
npx cap sync
npx cap open android    # Opens Android Studio
npx cap run android     # Runs on device
```

---

## 📄 License

MIT License - Feel free to use, modify and distribute.

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request.

---

Made with ❤️ by [josevdr95](https://github.com/josevdr95new)
