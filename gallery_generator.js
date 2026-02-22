let galleryState = {};

//get the page type - stoly/doplnky/etc. from an empty div at the top of the page
const typeDesignator = document.getElementById("gallery-type");
const galleryPage = typeDesignator.getAttribute("type");

fetch("dirmap.json")
    .then(response => response.json())
    .then(responseContent => {
        generateGalleries(responseContent, galleryPage); //subsection tells the generate galleries function, which folder should be used, i.e. stoly 
        //initGalleryData(responseContent, galleryPage);
    }) 
    .catch(error => console.error("Error generating galleries: ", error));

function preloadImage(src) 
{
    const img = new Image();
    img.src = src;
}

function initGalleryData(galleryName, imgPaths)
{
    galleryState[galleryName] = {
        activeIndex: 0,
        imagePaths: imgPaths,
        size: Object.keys(imgPaths).length,
    };
    console.log(galleryState)
}

function generateGalleries(dirmap, galleryPage)
{
    const workingFolder = dirmap[galleryPage]; //select the folder relevant for the current page i.e. "/stoly/"
    const container = document.getElementsByClassName("container")[0]; //container that will contain the galleries
    container.innerHTML = "";

    Object.keys(workingFolder).forEach(galleryName => {
        const galleryContent = workingFolder[galleryName].items;
        const galleryText = workingFolder[galleryName].text
        let imgPaths = {};
        //console.log(galleryName);
        //console.log(galleryContent);
        //console.log(galleryText);
        
        //create the main gallery div
        const galleryDiv = document.createElement("div");
        galleryDiv.setAttribute("class", "gallery");
        galleryDiv.setAttribute("id", `gallery_${galleryName}`);

        //create the inner gallery div (items wrapper)
        const itemsWrapperDiv = document.createElement("div");
        itemsWrapperDiv.setAttribute("class", "items_wrapper");
        itemsWrapperDiv.setAttribute("id", `items_${galleryName}`);
        
        //create the navigation summary of images
        const itemsPreviewWrapperDiv = document.createElement("div");
        itemsPreviewWrapperDiv.setAttribute("class", "preview_row");
        itemsPreviewWrapperDiv.setAttribute("id", `preview_row_${galleryName}`);

        //add individual items to the items wrapper and to the preview row
        Object.keys(galleryContent).forEach(imageIndex => {
            //create the image element (<img>)
            const imagePath = `/galerie/${galleryPage}/${galleryName}/processed/${galleryContent[imageIndex]}`; //galleryContent[imageIndex] is the name of the image
            imgPaths[imageIndex] = imagePath; // add the paths of full-sized imgs to this array. 
            //const imageElement = document.createElement("img");
            //imageElement.setAttribute("src", imagePath); 
            //imageElement.loading = "eager";
            //preloadImage(imagePath);  
            
            const thumbnailPath = `/galerie/${galleryPage}/${galleryName}/thumbnails/${galleryContent[imageIndex]}`;
            const thumbnailElement = document.createElement("img");
            thumbnailElement.setAttribute("src", thumbnailPath);   

            
            const itemPreviewDiv = document.createElement("div");

            if(imageIndex == 0)
            {
                const imageElement = document.createElement("img");
                imageElement.setAttribute("src", imagePath); 
                const itemDiv = document.createElement("div");
                itemDiv.setAttribute("class", "item");
                itemDiv.setAttribute("id", `item_${galleryName}`);
                itemDiv.append(imageElement);
                itemsWrapperDiv.appendChild(itemDiv);
                //itemDiv.classList.add("active");
            }

            itemPreviewDiv.setAttribute("class", "row_item");
            itemPreviewDiv.setAttribute("id", `row_item_${galleryName}`);
            itemPreviewDiv.dataset.parentGallery = galleryName;
            itemPreviewDiv.dataset.imageIndex = imageIndex;
            if(imageIndex == 0){itemPreviewDiv.classList.add("active");}

            itemPreviewDiv.append(thumbnailElement);

            itemsPreviewWrapperDiv.appendChild(itemPreviewDiv);
        });
        galleryDiv.appendChild(itemsWrapperDiv);

        //add the prev & next buttons
        const prev = document.createElement("div");
        prev.setAttribute("class", "prev");
        prev.setAttribute("id", `prev_${galleryName}`);
        prev.dataset.parentGallery = galleryName;
        prev.innerHTML = "<p>&#10094;</p>";
        galleryDiv.appendChild(prev);
        
        const next = document.createElement("div");
        next.setAttribute("class", "next");
        next.setAttribute("id", `next_${galleryName}`);
        next.dataset.parentGallery = galleryName;
        next.innerHTML = "<p>&#10095;</p>";
        galleryDiv.appendChild(next);
        
        //create and add the info box
        const infoBox = document.createElement("div");
        infoBox.setAttribute("class", "info");
        infoBox.setAttribute("id", `info_${galleryName}`);
        
        if (galleryText != null)
        {
            Object.keys(galleryText).forEach(line_index => {
                line = galleryText[line_index];
                const line_div = document.createElement("div");
                line_div.innerHTML = line;
                infoBox.appendChild(line_div);
            });
        }

        galleryDiv.appendChild(infoBox);

        //append the preview row that was created earlier
        galleryDiv.appendChild(itemsPreviewWrapperDiv);

        //append the whole gallery to the container
        container.appendChild(galleryDiv);

        //init the gallery data
        console.log(imgPaths)
        initGalleryData(galleryName, imgPaths)
    });
}
