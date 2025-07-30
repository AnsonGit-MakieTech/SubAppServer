
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












