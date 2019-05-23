---
titlepage: true
title: "Projet : Automate F5 Application Delivery Controller configuration via REST"
subtitle: "VIRI"
author: [Sylvain Renaud]
date: \today
toc: true
toc-own-page: true
logo: "logo-hes-so.jpg"
logo-width: 200
---

# Configutation de Vagrant

Tout d'abord, on va utiliser la box `boeboe/F5-BIGIP` ([https://app.vagrantup.com/boeboe/boxes/F5-BIGIP](https://app.vagrantup.com/boeboe/boxes/F5-BIGIP)). Pour la démarrer, il suffit de faire les commandes suivantes:

```bash
vagrant init boeboe/F5-BIGIP
vagrant up
```

Un fois la machine démarrée, on peut accéder à son interface web via <https://localhost:10443/xui/>. Les credentials par défaut pour se connecter sont **vagrant/vagrant**

# Application