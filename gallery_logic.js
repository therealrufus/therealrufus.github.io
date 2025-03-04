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
    //console.log(galleryName);
    //console.log(galleryState[galleryName]);

    const gallerySize = galleryState[galleryName].totalImages;
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

    const itemsWrapper = document.getElementById(`items_${galleryName}`);
    const items = itemsWrapper.querySelectorAll('.item');
    const activeItem = items[activeIndex];
    const newActiveItem = items[newActiveIndex];

    const itemsPreviewWrapper = document.getElementById(`preview_row_${galleryName}`);
    const previewItems = itemsPreviewWrapper.querySelectorAll('.row_item');
    const activePreviewItem = previewItems[activeIndex];
    const newActivePreviewItem = previewItems[newActiveIndex];

    //unset the active item from being active
    activeItem.classList.remove("active");
    newActiveItem.classList.add("active");

    activePreviewItem.classList.remove("active");
    newActivePreviewItem.classList.add("active");

    galleryState[galleryName].activeIndex = newActiveIndex;
    console.log(galleryState[galleryName]);
}
