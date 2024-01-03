import './App.css'
import "primereact/resources/themes/lara-light-cyan/theme.css";

import { useEffect, useState } from 'react';

import { ProgressBar } from 'primereact/progressbar';
import { getApiUrl } from './utils';

interface CsvFile {
    id: number;
    file: string;
    status: string;
    progress: number;
    total: number;
    error_message: string | null;
    // Add other fields based on the actual CSV file structure
}

function App() {

    const fetchData = async () => {
        try {
            const response = await fetch(`${getApiUrl()}/v1/csv-files/`);
            if (response.ok) {
                const data = await response.json();
                setJobs(data.results as CsvFile[]); // Assuming results is an array of CsvFile
            } else {
                throw new Error('Failed to fetch data');
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        const interval = setInterval(fetchData, 1000);
        // Clear the interval when the component unmounts
        return () => clearInterval(interval);
    }, []); // Run this effect only once (on mount)

    const [jobs, setJobs] = useState<CsvFile[]>([]);

    return (
        <div className="wip">
            {jobs.map((job: CsvFile) => {
                return <div key={job.id} className="job">
                    <div>
                        JOB #{job.id} - {job.progress}% - {job.total} lignes - {job.status}
                    </div>
                    <div>
                        <ProgressBar value={job.progress}></ProgressBar>
                    </div>
                </div>
            })}
        </div>
    )
}

export default App

