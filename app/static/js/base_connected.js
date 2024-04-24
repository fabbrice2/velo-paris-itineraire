let pseudo = document.querySelector(".pseudo");
let profilSetting = document.querySelector(".profil-setting");
let profilSettingResponsiv = document.querySelector(".profil-setting-responsiv");
let close = document.querySelector(".profil-setting .close");
let closeResponsiv = document.querySelector(".profil-setting-responsiv .close-responsiv");
let menuBurger = document.querySelector(".menu-burger");


console.log(close);



pseudo.addEventListener('click' ,function () {
    
profilSetting.classList.toggle('active');
})

close.addEventListener('click' ,function () {
    
    profilSetting.classList.remove('active')
})



// ........................................................


menuBurger.addEventListener('click' ,function () {
    
    profilSettingResponsiv.classList.toggle('active');
    })
    
    closeResponsiv.addEventListener('click' ,function () {
        
        profilSettingResponsiv.classList.remove('active')
    })
    