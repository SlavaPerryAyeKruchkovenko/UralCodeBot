import {useState} from "react";
import "./App.css";
import {Button, Flex, Layout, Space} from "antd";
import {Routes} from "./types/routing";
import UploadPage from "./pages/UploadVIdeo/UploadPage";
import Main from "./pages/UploadVIdeo/Main";


function App() {
    const [route, setRoute] = useState(Routes.Main);

    const routeDictionary = {
        [Routes.UploadVideo]: <UploadPage/>,
        [Routes.Main]: <Main/>
    }

    return (
        <div style={{width: '100vw', height: '100vh', overflow: 'auto'}}>
            <Layout style={{width: '100%', height: '100%'}}>
                <Layout.Header style={{width: '100%', height: '60px'}}>
                    <Space>
                        <Button onClick={() => setRoute(Routes.UploadVideo)}>
                            Загрузить видео
                        </Button>
                        <Button onClick={() => setRoute(Routes.Main)}>
                            Обзор
                        </Button>
                    </Space>

                </Layout.Header>
                <Layout.Content>
                    <Space style={{overflowY: 'auto', width: '100%', height: '100%'}}>
                        {routeDictionary[route]}
                    </Space>
                </Layout.Content>
            </Layout>
        </div>
    );
}

export default App;
