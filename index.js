function getFreshestFiles() {
  return fetch('./resources/')
    .then((response) => response.text())
    .then((html) => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const links = doc.querySelectorAll('a[href$=".json"]');

      const freshestFiles = [];

      links.forEach((link) => {
        const fileName = link.textContent.split('/').pop().replace('.json', '');
        if (fileName.startsWith('heroes_') || fileName.startsWith('builds_')) {
          freshestFiles.push(fileName);
        }
      });

      const sortedFiles = freshestFiles.sort((a, b) => {
        const dateA = a.match(/\d{4}-\d{2}-\d{2}/);
        const dateB = b.match(/\d{4}-\d{2}-\d{2}/);

        if (dateA && dateB) {
          return new Date(dateB) - new Date(dateA);
        }
        return 0;
      });

      const fileName1 = sortedFiles[0];
      const fileName2 = sortedFiles[1];
      return [fileName1, fileName2];
    });
}

function calculateTotalAdvantage(mainHero, searchedHero, heroesDataset) {
  console.log(mainHero)
  console.log(searchedHero)
  const advantageData = heroesDataset[mainHero];
  console.log(parseFloat(advantageData[searchedHero]))
  return advantageData[searchedHero];
}

var xhr1 = new XMLHttpRequest();
var xhr2 = new XMLHttpRequest();

getFreshestFiles()
  .then(([fileName1, fileName2]) => {
    
    xhr1.open("GET", `./resources/${fileName2}.json`, true);
    xhr1.responseType = "json";
    xhr1.send(); 
    
    xhr2.open("GET", `./resources/${fileName1}.json`, true);
    xhr2.responseType = 'json';
    xhr2.send(); 
  })
  .catch((error) => {
    console.error('Error loading freshest files:', error);
  });

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

xhr2.onload = function() {
  if (xhr2.status === 200) {
    buildsDataset = xhr2.response; 
    document.querySelectorAll(".rDropdownsContainer select").forEach(function(selectElement) {
      selectElement.addEventListener("change", function() {
      const heroName = selectElement;
      const heroBuilds = document.querySelector(`.hero-builds .rHeroes .${heroName.title}`)

      heroBuilds.querySelectorAll(".start p, .main p").forEach(function(pElement) {
        pElement.remove();
      });

      if (heroName.value === "none") return;
      const heroBuildsData = buildsDataset[heroName.value];

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
    document.querySelectorAll(".dDropdownsContainer select").forEach(function(selectElement) {
      selectElement.addEventListener("change", function() {
        const heroName = selectElement;
        const heroBuilds = document.querySelector(`.hero-builds .dHeroes .${heroName.title}`)

        heroBuilds.querySelectorAll(".start p, .main p").forEach(function(pElement) {
          pElement.remove();
        });
        
        if (heroName.value === "none") return;
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

document.querySelectorAll(".dDropdownsContainer select").forEach(function(selectElement) {
  selectElement.addEventListener("change", function() {
    const rightHero = selectElement.value;
    document.querySelectorAll(".rDropdownsContainer select").forEach(function(otherElement) {
      const leftHero = otherElement.value
      if ((rightHero === "none") || (leftHero === "none") || (leftHero === rightHero)) return;
      const advantage = calculateTotalAdvantage(leftHero, rightHero, heroesDataset);
      console.log("Advantage:", advantage);
  
      // Clear the previous advantage text
      const advantageText = document.querySelector(".advantage");
      if (advantageText) {
        advantageText.textContent = "";
      }
  
      // Display the new advantage text
      const newAdvantageText = document.createElement("p");
      newAdvantageText.textContent = `Advantage: ${advantage}`;
      document.querySelector(".advantage").appendChild(newAdvantageText);

    })
  });
});

