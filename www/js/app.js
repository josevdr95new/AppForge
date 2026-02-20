const openExternalLink = async (url) => {
    if (window.Capacitor?.isNativePlatform?.()) {
        window.open(url, '_system');
    } else {
        window.open(url, '_blank');
    }
};

const parseDeepLink = (url) => {
    if (!url) return null;
    
    try {
        const urlObj = new URL(url);
        const scheme = urlObj.protocol.replace(':', '');
        const host = urlObj.hostname;
        const pathname = urlObj.pathname;
        const params = Object.fromEntries(urlObj.searchParams);
        
        const segments = pathname.split('/').filter(s => s);
        
        let route = {
            scheme,
            host,
            path: pathname,
            segments,
            params,
            action: null,
            data: {}
        };
        
        if (scheme === 'miapp' || host === 'miapp.com') {
            if (segments[0] === 'producto' && segments[1]) {
                route.action = 'view_product';
                route.data = { productId: segments[1], ...params };
            } else if (segments[0] === 'usuario' && segments[1]) {
                route.action = 'view_user';
                route.data = { username: segments[1], ...params };
            } else if (segments[0] === 'configuracion') {
                route.action = 'open_settings';
                route.data = { ...params };
            } else if (segments[0] === 'promo' && segments[1]) {
                route.action = 'view_promo';
                route.data = { codigo: segments[1], ...params };
            } else if (segments[0] === 'reset-password' && params.token) {
                route.action = 'reset_password';
                route.data = { token: params.token };
            } else if (segments[0] === 'verify-email' && params.token) {
                route.action = 'verify_email';
                route.data = { token: params.token };
            } else {
                route.action = 'home';
            }
        }
        
        console.log('Deep Link parsed:', route);
        return route;
    } catch (e) {
        console.error('Error parsing deep link:', e);
        return null;
    }
};

const handleDeepLinkRoute = (route) => {
    if (!route || !route.action) return;
    
    const deepLinkLog = document.getElementById('deep-link-log');
    
    switch (route.action) {
        case 'view_product':
            showToast(`Abriendo producto ID: ${route.data.productId}`);
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info">
                        <strong>Producto</strong><br>
                        ID: ${route.data.productId}<br>
                        ${route.data.ref ? 'Referencia: ' + route.data.ref : ''}
                    </div>
                `;
            }
            break;
            
        case 'view_user':
            showToast(`Abriendo perfil de: ${route.data.username}`);
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info">
                        <strong>Usuario</strong><br>
                        Username: @${route.data.username}
                    </div>
                `;
            }
            break;
            
        case 'open_settings':
            showToast('Abriendo configuración');
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info">
                        <strong>Configuración</strong><br>
                        Tab: ${route.data.tab || 'general'}
                    </div>
                `;
            }
            break;
            
        case 'view_promo':
            showToast(`¡Promoción: ${route.data.codigo}!`);
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info" style="background: #4CAF50; color: white; padding: 15px; border-radius: 8px;">
                        <strong>🎉 Promoción Especial</strong><br>
                        Código: ${route.data.codigo}<br>
                        ${route.data.descuento ? 'Descuento: ' + route.data.descuento + '%' : ''}
                    </div>
                `;
            }
            break;
            
        case 'reset_password':
            showToast('Restableciendo contraseña...');
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info" style="background: #2196F3; color: white; padding: 15px; border-radius: 8px;">
                        <strong>🔐 Restablecer Contraseña</strong><br>
                        Token: ${route.data.token.substring(0, 8)}...
                    </div>
                `;
            }
            break;
            
        case 'verify_email':
            showToast('Verificando email...');
            if (deepLinkLog) {
                deepLinkLog.innerHTML = `
                    <div class="deep-link-info" style="background: #9C27B0; color: white; padding: 15px; border-radius: 8px;">
                        <strong>✉️ Verificación de Email</strong><br>
                        Procesando...
                    </div>
                `;
            }
            break;
            
        default:
            console.log('Unknown deep link action:', route.action);
    }
};

const initDeepLinks = async () => {
    const App = window.Capacitor?.Plugins?.App;
    
    if (!App) {
        console.log('App plugin not available');
        return;
    }
    
    App.addListener('appUrlOpen', (data) => {
        console.log('Deep Link received:', data.url);
        const route = parseDeepLink(data.url);
        if (route) {
            handleDeepLinkRoute(route);
        }
    });
    
    const coldStart = await App.getState();
    if (coldStart?.url) {
        console.log('App started with URL:', coldStart.url);
        const route = parseDeepLink(coldStart.url);
        if (route) {
            setTimeout(() => handleDeepLinkRoute(route), 500);
        }
    }
};

const bindExternalLinks = () => {
    document.querySelectorAll('.external-url').forEach(link => {
        link.onclick = async (e) => {
            e.preventDefault();
            const url = link.getAttribute('data-url');
            if (url) await openExternalLink(url);
        };
    });
};

const saveData = async (key, data) => {
    if (window.Capacitor?.Plugins?.Preferences) {
        await window.Capacitor.Plugins.Preferences.set({ key, value: JSON.stringify(data) });
    } else {
        localStorage.setItem(key, JSON.stringify(data));
    }
};

const loadData = async (key, defaultValue = null) => {
    try {
        if (window.Capacitor?.Plugins?.Preferences) {
            const { value } = await window.Capacitor.Plugins.Preferences.get({ key });
            return value ? JSON.parse(value) : defaultValue;
        } else {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : defaultValue;
        }
    } catch {
        return defaultValue;
    }
};

const showToast = async (message) => {
    if (window.Capacitor?.Plugins?.Toast) {
        await window.Capacitor.Plugins.Toast.show({ text: message, duration: 'short' });
    } else {
        alert(message);
    }
};

const takePhoto = async () => {
    if (!window.Capacitor?.Plugins?.Camera) {
        showToast('Camera no disponible');
        return null;
    }
    try {
        const photo = await window.Capacitor.Plugins.Camera.getPhoto({
            quality: 90,
            allowEditing: false,
            resultType: 'base64',
            source: 'CAMERA'
        });
        return `data:image/${photo.format};base64,${photo.base64String}`;
    } catch (error) {
        console.error('Error al tomar foto:', error);
        return null;
    }
};

const pickImage = async () => {
    if (!window.Capacitor?.Plugins?.Camera) {
        showToast('Camera no disponible');
        return null;
    }
    try {
        const photo = await window.Capacitor.Plugins.Camera.getPhoto({
            quality: 90,
            allowEditing: false,
            resultType: 'base64',
            source: 'PHOTOS'
        });
        return `data:image/${photo.format};base64,${photo.base64String}`;
    } catch (error) {
        console.error('Error al seleccionar imagen:', error);
        return null;
    }
};

const getLocation = async () => {
    if (!window.Capacitor?.Plugins?.Geolocation) {
        showToast('Geolocation no disponible');
        return null;
    }
    try {
        const position = await window.Capacitor.Plugins.Geolocation.getCurrentPosition();
        return {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
        };
    } catch (error) {
        console.error('Error al obtener ubicacion:', error);
        return null;
    }
};

const getNetworkStatus = async () => {
    if (window.Capacitor?.Plugins?.Network) {
        try {
            return await window.Capacitor.Plugins.Network.getStatus();
        } catch (error) {
            return { connected: navigator.onLine, connectionType: 'unknown' };
        }
    }
    return { connected: navigator.onLine, connectionType: 'unknown' };
};

const fetchData = async (url, options = {}) => {
    try {
        const response = await fetch(url, {
            ...options,
            cache: 'no-cache'
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
};

const loadAppConfig = async () => {
    try {
        const response = await fetch('app.config.json');
        return await response.json();
    } catch (error) {
        console.error('Error al cargar configuracion:', error);
        return null;
    }
};

const initApp = async () => {
    console.log('App lista');
    bindExternalLinks();
    
    if (window.Capacitor?.Plugins?.SplashScreen) {
        try {
            await window.Capacitor.Plugins.SplashScreen.hide();
        } catch (e) {
            console.log('SplashScreen no disponible');
        }
    }
    
    if (window.Capacitor?.Plugins?.StatusBar) {
        try {
            await window.Capacitor.Plugins.StatusBar.setStyle({ style: 'Dark' });
            await window.Capacitor.Plugins.StatusBar.setBackgroundColor({ color: '#ffffff' });
        } catch (e) {
            console.log('StatusBar no disponible');
        }
    }

    const config = await loadAppConfig();
    if (config) {
        const versionEl = document.getElementById('app-version');
        if (versionEl) {
            versionEl.textContent = `v${config.version} (${config.versionCode})`;
        }
    }

    window.takePhoto = takePhoto;
    window.pickImage = pickImage;
    window.getLocation = getLocation;
    window.getNetworkStatus = getNetworkStatus;
    window.showToast = showToast;
    window.saveData = saveData;
    window.loadData = loadData;
    window.openExternalLink = openExternalLink;
    window.parseDeepLink = parseDeepLink;
    window.handleDeepLinkRoute = handleDeepLinkRoute;
    
    await initDeepLinks();
};

document.addEventListener('DOMContentLoaded', initApp);
