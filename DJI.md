Este es el documento técnico para el proyecto DJI.

Version de odoo : 12.0

**Datos del servidor**

L'adresse IPv4 du VPS est : 51.83.185.120

Nom d'utilisateur : ubuntu

Mot de passe :      SADAHjv2aDWh

**Base de datos**

dji

**Usuarios**

usuario : contabilidad@distribucionesjoaquininfante.es

password: m!od&bPGDS43dSCEKPJtxZkLqsp2FHHT8JWivwajsgNB23V)twr#S4m&

mail_password : Xtend00!

---

usuario : admin

password : sVWC!ogF!5nYiZgygtW9AHGfYnX5)8YrK3hUbtQ(&naZo2QUKiRktc)M

mail : odoo@distribucionesjoaquininfante.es

password : sVWC!ogF!5nYiZgygtW9

---

**Aplicaciones instaladas:**

base.module_website

base.module_stock

base.module_account

base.module_sale_management

base.module_website_sale

base.module_purchase

base.module_mail

base.module_website_livechat

base.module_im_livechat

account_cancel

España - Contabilidad (PGCE 2008)


**Módulos instalados:**

https://github.com/OCA/product-attribute/tree/12.0/product_brand

https://github.com/OCA/e-commerce/tree/12.0/website_sale_hide_price

https://github.com/OCA/web/tree/12.0/web_pwa_oca

https://github.com/OCA/web/tree/12.0/web_decimal_numpad_dot

https://github.com/OCA/web/tree/12.0/web_company_color

Fichero : addons.yaml

l10n-spain: ["*"]
product-attribute:
    - product_brand
server-ux:
    - mass_editing
web: ["*"]
website: ["*"]
e-commerce:
    - website_sale_hide_price
stock-logistics-barcode: ["*"]
---
# Custom repositories
ENV:
    DEFAULT_REPO_PATTERN: https://github.com/xtendoo-corporation/{}.git
    ODOO_VERSION: 12.0
xtendoo: ["*"]



