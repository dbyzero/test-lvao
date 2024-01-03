import './App.css'
import "primereact/resources/themes/lara-light-cyan/theme.css";

import { Button } from 'primereact/button';
import { PrimeReactProvider } from 'primereact/api';
import Uploader from './Uploader';
import WorkInProgress from './WorkInProgress';
import { classNames } from 'primereact/utils';
import { getApiUrl } from './utils';

function App() {

    const downloadData = async () => {
        try {
            const response = await fetch(`${getApiUrl()}/v1/download-csv/`);
            if (!response.ok) {
                throw new Error('Failed to download CSV');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'exported_data.csv');
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);
        } catch (error) {
            console.error('Error downloading CSV:', error);
            // Handle error (e.g., show an error message to the user)
        }
    }

    return (
        <PrimeReactProvider>
            <div className="main">
                <div className="header">
                    <h1>Test longue vie aux objets</h1>
                    <h2>Cyril ALFARO - 2024</h2>
                </div>
                <Uploader />
                <WorkInProgress />
            </div>
            <div className="download-data">
                <Button
                    severity="info" rounded
                    label="Télécharger la data validée"
                    icon="pi pi-download"
                    iconPos="right"
                    className={classNames('p-button-raised p-button-success')}
                    onClick={downloadData}
                    style={{ backgroundColor: '#333' }}
                />
            </div>
        </PrimeReactProvider>
    )
}

export default App
