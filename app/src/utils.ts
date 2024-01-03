export const uploadFile = () => {

};

export const getApiUrl = () => {
    let baseURL = `${window.location.protocol}//api.${window.location.hostname}`
    if (window.location.hostname === 'localhost') {
        baseURL = `http://api.lvao-test.dbyzero.com`
        // baseURL = `http://localhost`
    }
    return baseURL
}