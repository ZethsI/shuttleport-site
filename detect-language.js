// detect-language.js
(function() {
    const userLang = navigator.language || navigator.userLanguage;
    const langPrefix = userLang.substring(0, 2); // Kullanıcının dilini algılar (örn. "en", "es", "ja")

    // Dil tespiti ve yönlendirme işlemi
    if (langPrefix === 'en') {
        window.location.href = "/index-en.html";
    } else if (langPrefix === 'es') {
        window.location.href = "/index-es.html";
    } else if (langPrefix === 'ja') {
        window.location.href = "/index-ja.html";
    } else {
        window.location.href = "/index-en.html";  // Varsayılan olarak İngilizceye yönlendir
    }
})();
