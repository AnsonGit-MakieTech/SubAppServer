
var controller = null;
async function connecting_to_api_with_global_abort(data ) {
    // Abort previous request if it exists
    if (controller) {
        controller.abort();
    }

    controller = new AbortController(); 
    const signal = controller.signal; 

    let has_popup = true; 
    if (data && Object.keys(data).length > 0) {
        if ('noerror' in data) {
            delete data.noerror;
            has_popup = false;
        }
    } 

    try{
        const formData = new FormData();  
        formData.append('data', JSON.stringify(data));

        const response = await fetch('../api/callback', {
            method: 'POST',
            headers: { 
                'X-CSRFToken': csrftoken,
            },
            body: formData,
            signal: signal,
        });

        if (response.ok) {
            const result = await response.json();
            return result;
        } else {
            const error = await response.json();
            if (has_popup){
                error_display_opener(error.text);    
            } 
            return null;
        }
    } catch (error) {
        if (error?.name === 'AbortError') {
            console.warn("🚫 Request was aborted");
            return null;
        } else {
            return null;
        }
    }
}



async function connecting_to_api( data ){
    let has_popup = true;
    // First, ensure data is defined and not null, and check if it has any keys
    if (data && Object.keys(data).length > 0) {
        // For example, remove "actions" only if it exists
        if ('noerror' in data) {
            delete data.noerror;
            has_popup = false;
        }
    } 

    try{
        const formData = new FormData(); 
        // Example of data structure data = { 'actions': 'action' , ....}
        formData.append('data', JSON.stringify(data));
 
        const response = await fetch('../api/callback', {
            method: 'POST',
            headers: { 
                'X-CSRFToken': csrftoken,
            },
            body: formData
        });
        const contentType = response.headers.get('Content-Type');
        // console.log((contentType && contentType.includes('application/json') ))
        if (response.ok) {
            // const result = await response.json();
            // return result;
            if (contentType && contentType.includes('application/json')) {
                const result = await response.json();
                return result;
            } else {
                // Assume it's a file (PDF, etc.)
                const blob = await response.blob();
                const fileURL = URL.createObjectURL(blob);

                // Create a temporary <a> element to trigger download
                const a = document.createElement('a');
                a.href = fileURL;
                const filename = fileURL.split('/').pop(); 
                a.download = filename;  // You can customize the filename
                document.body.appendChild(a);
                a.click();
                a.remove();

                // Optionally revoke the URL after download to free memory
                URL.revokeObjectURL(fileURL);
                return {'text' : 'Please wait for the file to be downloaded.'};
            }
        } else {
            // const error = await response.json();
            // if (has_popup){
            //     error_display_opener(error.text);    
            // } 
            // return null;
            if (contentType && contentType.includes('application/json')) {
                const error = await response.json();
                if (has_popup) error_display_opener(error.text);
            } else {
                if (has_popup) error_display_opener("An unknown error occurred.");
            }
            return null;
        }
    } catch (error) {
        return null;
    }
    
}


async function connecting_to_unsafe_api( data ){
    let has_popup = false;
    // First, ensure data is defined and not null, and check if it has any keys
    if (data && Object.keys(data).length > 0) {
        // For example, remove "actions" only if it exists
        if ('noerror' in data) {
            delete data.noerror;
            has_popup = true;
        }
    } 

    try{
        
        const formData = new FormData(); 
        // Example of data structure data = { 'actions': 'action' , ....}
        formData.append('data', JSON.stringify(data));

        const response = await fetch('../api/unauthenticated_api', {
            method: 'POST',
            headers: { 
                'X-CSRFToken': csrftoken,
            },
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            return result;
        } else {
            const error = await response.json();
            if (has_popup == false){
                error_display_opener(error.text);    
            } 
            return null;
        }
    } catch (error) {
        return null;
    }
    
}




function reAnimateElement(element, animationClass, display = 'flex') {
    if (!element) {
        console.warn("⚠️ Element not found.");
        return;
    }

    // Step 1: Make it visible (before animation)
    element.style.display = display;

    // Step 2: Temporarily remove the animation class
    element.classList.remove(animationClass);

    // Step 3: Force reflow to reset animation
    void element.offsetWidth;

    // Step 4: Re-add animation class
    element.classList.add(animationClass); 
}
 
function hideModal(element , animationClass ) {
    if (element) {
        element.style.display = 'none';
        element.classList.remove(animationClass);
    }
}











// /* ========================================== This is the pop up format for reference  */
// @keyframes fadeIn {
//     0% {
//         opacity: 0;
//         transform:  translateY(20px);
//     }
//     100%{
//         opacity: 1;
//         transform:  translateY(0px);
//     }
// }

// .pop-up-container-animate-in {
//     animation: fadeIn 0.3s ease-out forwards; 
// }


// .pop-up-container{  
//     display: none;
//     /* display: flex; */
//     position: fixed;
//     width: 100%;
//     height: 100svh; 
//     top: 0;
//     background: rgba(236, 246, 251, 0.5);
//     z-index: 50;
//     justify-content: center;
//     align-items: center;
//     overflow-x: hidden;
//     overflow-y: scroll;
//     padding: 15px;
 
// }

// .pop-up-wrapper{ 
//     min-width: 600px;
//     width: fit-content;
//     height: fit-content;  
//     max-width: 70vw;
//     background: #FFFDFA;
//     border: 4px solid #181C1D;
//     border-radius: 8px; 
//     margin: 15px;
//     display: flex;
//     flex-direction: column;
//     justify-content: flex-start;
//     align-items: center;
//     padding-bottom: 20px;
// }
