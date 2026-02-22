document.addEventListener("click", function (event)
{   
    const galleryName = event.target.getAttribute('data-parent-gallery');
    const rowItem = event.target.closest(".row_item");

    if (event.target.matches(".prev")) 
    {
        chengeActive(galleryName, -1, "advance");
    } 
    else if (event.target.matches(".next")) 
    {
        chengeActive(galleryName, 1, "advance");
    }
    else if (rowItem)
    {
        const galleryName = rowItem.getAttribute('data-parent-gallery');
        const imageIndex = rowItem.getAttribute('data-image-index');

        chengeActive(galleryName, parseInt(imageIndex), "select");
    }
});

//argument is either -1/+1 for advancing by one, or the index of the new active item.
function chengeActive(galleryName, argument, mode)
{
    const gallerySize = galleryState[galleryName].size;
    const activeIndex = galleryState[galleryName].activeIndex;
    var newActiveIndex = 0;
    
    //get new index, depending on mode of invocation
    if (mode == "advance")
    {
        if(activeIndex + argument == gallerySize)
        {
            newActiveIndex = 0;
        }
        else if(activeIndex + argument < 0)
        {
            newActiveIndex = gallerySize - 1;
        }
        else
        {
            newActiveIndex = activeIndex + argument;
        }
    }
    else if (mode == "select")
    {
        newActiveIndex = argument; 
    }

    //get new active thumbnail
    const itemsPreviewWrapper = document.getElementById(`preview_row_${galleryName}`);
    const previewItems = itemsPreviewWrapper.querySelectorAll('.row_item');
    const activePreviewItem = previewItems[activeIndex];
    const newActivePreviewItem = previewItems[newActiveIndex];

    activePreviewItem.classList.remove("active");
    newActivePreviewItem.classList.add("active");

    //change the src of the main image
    const container = document.getElementById(`item_${galleryName}`);
    const imgElement = container.querySelector("img");

    const temp = new Image();
    newSrc = galleryState[galleryName].imagePaths[newActiveIndex];
    temp.src = newSrc;
    temp.onload = () => {
        imgElement.src = newSrc;
    };
    

    galleryState[galleryName].activeIndex = newActiveIndex;
}
