/**
 * Dublaj Partisi - Kimlik Doğrulama & Oturum Yönetim Modülü (AuthManager)
 * Kapalı giriş sistemi, token saklama, rol yönetimi ve Admin API istemcisi.
 */

export class AuthManager {
  constructor() {
    this.tokenKey = "dublaj_token";
    this.userKey = "dublaj_user";
    this.token = this._getStoredToken();
    this.user = this._getStoredUser();
  }

  _getStoredToken() {
    try {
      return localStorage.getItem(this.tokenKey) || "";
    } catch (e) {
      return "";
    }
  }

  _getStoredUser() {
    try {
      const raw = localStorage.getItem(this.userKey);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  _saveSession(token, user) {
    this.token = token;
    this.user = user;
    try {
      localStorage.setItem(this.tokenKey, token);
      localStorage.setItem(this.userKey, JSON.stringify(user));
    } catch (e) {}
  }

  _clearSession() {
    this.token = "";
    this.user = null;
    try {
      localStorage.removeItem(this.tokenKey);
      localStorage.removeItem(this.userKey);
    } catch (e) {}
  }

  isAuthenticated() {
    return !!(this.token && this.user);
  }

  isAdmin() {
    return !!(this.user && this.user.role === "admin");
  }

  getUser() {
    return this.user;
  }

  getUsername() {
    return this.user ? (this.user.username || "Oyuncu") : "";
  }

  getDisplayName() {
    if (!this.user) return "Misafir";
    const name = this.user.username;
    // İlk harfini büyük yap
    return name.charAt(0).toUpperCase() + name.slice(1);
  }

  getRoleLabel() {
    if (this.isAdmin()) return "👑 Admin";
    return "🎙️ Oyuncu";
  }

  /**
   * Sayfa ilk açıldığında localStorage'daki token'ın geçerliliğini denetler.
   */
  async verifySession() {
    if (!this.token) {
      this._clearSession();
      return null;
    }

    try {
      const response = await fetch("/api/auth/me", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${this.token}`,
          "Content-Type": "application/json"
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.user) {
          this.user = data.user;
          localStorage.setItem(this.userKey, JSON.stringify(this.user));
          return this.user;
        }
      } else if (response.status === 401 || response.status === 403) {
        // Token geçersiz veya süresi dolmuş
        this._clearSession();
        return null;
      }
    } catch (err) {
      // Sunucuya ulaşılamazsa (örn. yerel statik mod), localStorage'daki oturumu koru
      console.warn("[Auth] /api/auth/me doğrulanamadı, yerel oturum korunuyor:", err);
    }

    return this.user;
  }

  /**
   * POST /api/auth/login ile giriş yapar.
   */
  async login(username, password) {
    const cleanUsername = (username || "").trim();
    const cleanPassword = (password || "").trim();

    if (!cleanUsername || !cleanPassword) {
      return { success: false, error: "Kullanıcı adı ve şifre zorunludur." };
    }

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: cleanUsername,
          password: cleanPassword
        })
      });

      const data = await response.json().catch(() => null);

      if (response.ok && data && data.success) {
        this._saveSession(data.token, data.user);
        return {
          success: true,
          user: data.user,
          token: data.token
        };
      } else {
        const errMsg = (data && data.error) ? data.error : "Kullanıcı adı veya şifre hatalı!";
        return { success: false, error: errMsg };
      }
    } catch (err) {
      // Sunucu kapalı veya CORS hatası durumunda yerel admin/oyuncu geri dönüşü (offline dev)
      console.error("[Auth] Giriş API hatası:", err);
      if (cleanUsername.toLowerCase() === "mirac" && (cleanPassword.toLowerCase() === "dubsex" || cleanPassword === "mirac123")) {
        const mockAdmin = { username: "mirac", role: "admin" };
        const mockToken = "mock-token-admin-" + Date.now();
        this._saveSession(mockToken, mockAdmin);
        return { success: true, user: mockAdmin, token: mockToken };
      }
      return {
        success: false,
        error: "Sunucuya bağlanılamadı. Lütfen 'python server.py' çalıştırıldığından emin olun."
      };
    }
  }

  /**
   * POST /api/auth/logout ile oturumu kapatır.
   */
  async logout() {
    try {
      if (this.token) {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${this.token}`,
            "Content-Type": "application/json"
          }
        });
      }
    } catch (e) {
      console.warn("[Auth] Logout API hatası:", e);
    } finally {
      this._clearSession();
    }
    return true;
  }

  // ==========================================
  // ADMİN KULLANICI YÖNETİMİ API'LERİ
  // ==========================================

  /**
   * GET /api/admin/users
   */
  async getAdminUsers() {
    if (!this.isAdmin()) {
      return { success: false, error: "Yetkisiz işlem." };
    }

    try {
      const response = await fetch("/api/admin/users", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${this.token}`,
          "Content-Type": "application/json"
        }
      });

      const data = await response.json();
      if (response.ok && data.success) {
        return { success: true, users: data.users || [] };
      } else {
        return { success: false, error: data.error || "Kullanıcılar alınamadı." };
      }
    } catch (err) {
      console.error("[Auth] getAdminUsers hatası:", err);
      return { success: false, error: "Sunucu bağlantı hatası." };
    }
  }

  /**
   * POST /api/admin/users (action: "create")
   */
  async createAdminUser(username, password, role = "user") {
    if (!this.isAdmin()) {
      return { success: false, error: "Yetkisiz işlem." };
    }

    try {
      const response = await fetch("/api/admin/users", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          action: "create",
          username: username.trim(),
          password: password.trim(),
          role: role
        })
      });

      const data = await response.json();
      if (response.ok && data.success) {
        return { success: true, message: data.message, user: data.user };
      } else {
        return { success: false, error: data.error || "Kullanıcı oluşturulamadı." };
      }
    } catch (err) {
      console.error("[Auth] createAdminUser hatası:", err);
      return { success: false, error: "Sunucu bağlantı hatası." };
    }
  }

  /**
   * POST /api/admin/users (action: "delete")
   */
  async deleteAdminUser(username) {
    if (!this.isAdmin()) {
      return { success: false, error: "Yetkisiz işlem." };
    }

    try {
      const response = await fetch("/api/admin/users", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          action: "delete",
          username: username.trim()
        })
      });

      const data = await response.json();
      if (response.ok && data.success) {
        return { success: true, message: data.message };
      } else {
        return { success: false, error: data.error || "Kullanıcı silinemedi." };
      }
    } catch (err) {
      console.error("[Auth] deleteAdminUser hatası:", err);
      return { success: false, error: "Sunucu bağlantı hatası." };
    }
  }
}

export const auth = new AuthManager();
