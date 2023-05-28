var xhr1 = new XMLHttpRequest();

xhr1.open("GET", "./resources/heroes_2023-05-28_06-15.json", true);

xhr1.responseType = "json";

xhr1.onload = function() {
    if (xhr1.status === 200) {
        heroesDataset = xhr1.response; 
        const rContainer = document.querySelector(".rDropdownsContainer");
        const dContainer = document.querySelector(".dDropdownsContainer");

        const rHeroSelects = rContainer.querySelectorAll("select[title^='rHero']");
        const dHeroSelects = dContainer.querySelectorAll("select[title^='dHero']");

      // Iterate through the heroesDataset object
        Object.keys(heroesDataset).forEach(function(heroName, index) {
        // Get the corresponding <select> element for the current hero
        const option = document.createElement("option");
        option.textContent = heroName;
        option.value = heroName;

        // Append the option to all <select> elements
        rHeroSelects.forEach(function(select) {
          select.appendChild(option.cloneNode(true));
        });
        dHeroSelects.forEach(function(select) {
          select.appendChild(option.cloneNode(true));
        });
        });
    }
};

xhr1.send(); 

var xhr2 = new XMLHttpRequest()
xhr2.open("GET", "./resources/builds_2023-05-28_06-15.json", true);
xhr2.responseType = 'json';
xhr2.onload = function() {
    if (xhr2.status === 200) {
        buildsDataset = xhr2.response; 
        document.querySelectorAll(".rDropdownsContainer select").forEach(function(selectElement) {
            selectElement.addEventListener("change", function() {
            const heroName = selectElement;
            const heroBuilds = document.querySelector(`.hero-builds .rHeroes .${heroName.title}`)
            if (heroName === "none") return;

            const heroBuildsData = buildsDataset[heroName.value];

        // Loop through the heroBuildsData properties and display their values
            for (const category in heroBuildsData) {
                const categoryData = heroBuildsData[category];
                
                const appendix = heroBuilds.querySelector(`.${category}`);

                for (const item in categoryData) {
                    const itemData = categoryData[item];
                    const textData = document.createElement("p");
                    textData.textContent = `${item}: ${JSON.stringify(itemData)}`;
                    appendix.appendChild(textData);
                }
                heroBuilds.appendChild(appendix)
            }
    });
});
}
}
xhr2.send()