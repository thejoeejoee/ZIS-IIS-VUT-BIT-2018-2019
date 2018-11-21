export default function () {
    document.querySelectorAll('img.svg').forEach(function (img) {
        let imgID = img.id;
        let imgClass = img.className;
        const imgURL = img.src;
        const imgWidth = img.width;
        const imgHeight = img.height;

        fetch(imgURL).then(function (response) {
            return response.text();
        }).then(function (text) {

            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(text, "text/xml");

            // Get the SVG tag, ignore the rest
            const svg = xmlDoc.getElementsByTagName('svg')[0];

            // Add replaced image's ID to the new SVG
            if (typeof imgID !== 'undefined') {
                svg.setAttribute('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if (typeof imgClass !== 'undefined') {
                svg.setAttribute('class', imgClass + ' replaced-svg');
            }

            // Remove any invalid XML tags as per http://validator.w3.org
            svg.removeAttribute('xmlns:a');

            // Check if the viewport is set, if the viewport is not set the SVG wont't scale.
            if (!svg.getAttribute('viewBox') && svg.getAttribute('height') && svg.getAttribute('width')) {
                svg.setAttribute('viewBox', '0 0 ' + svg.getAttribute('height') + ' ' + svg.getAttribute('width'))
            }
            if (imgHeight) {
                svg.setAttribute('height', imgHeight)
            }
            if (imgWidth) {
                svg.setAttribute('width', imgWidth)
            }

            // Replace image with new SVG
            img.parentNode.replaceChild(svg, img);
        });
    });
};