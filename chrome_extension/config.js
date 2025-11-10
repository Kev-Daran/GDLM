const CONFIG = {
    API_URL_LOCAL: 'http://localhost:8000',
    API_URL_PROD: 'https://gdlm-backend-921940411855.europe-west1.run.app',   //IMP: Change to your production API URL on cloud run

    get API_URL() {
        return this.API_URL_LOCAL; //IMP: Change to API_URL_PROD before deployment
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}