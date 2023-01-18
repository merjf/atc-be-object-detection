import { useState } from "react";
import { makeStyles } from "@mui/styles";
import { Box, Container, Tab, Tabs } from "@mui/material";
import Header from './components/Header'
import Footer from './components/Footer'
import TabPanel from './components/TabPanel'
import CarDetection from './pages/CarDetection'
import MusicRecommandation from './pages/MusicRecommandation'
import AppRecommandation from './pages/AppRecommandation'

const useStyles = makeStyles({
  main: {
    marginTop: 100,
    marginBottom: 100,
    "& > nav": {
      marginBottom: 50
    }
  },
});

function App() {
  const classes = useStyles();

  const [currentTab, setCurrentTab] = useState(0);

  const handleChangeTab = (event: React.SyntheticEvent, newTab: number) => {
    setCurrentTab(newTab);
  };

  const tabPanelProps = (index : number) => {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  return (
    <div className="App">
      <Header />
      <Container maxWidth={"lg"} className={classes.main}>
        <Box component="nav" sx={{ borderBottom: 1, borderColor: 'divider' }} >
          <Tabs value={currentTab} onChange={handleChangeTab} aria-label="Services" centered>
            <Tab label="Car Detection" {...tabPanelProps(0)}/>
            <Tab label="Music Recommendation" {...tabPanelProps(1)}/>
            <Tab label="Play Store App Recommendation" {...tabPanelProps(2)}/>
          </Tabs>
        </Box>
        <TabPanel currentTab={currentTab} index={0}>
          <CarDetection />
        </TabPanel>
        <TabPanel currentTab={currentTab} index={1}>
          <MusicRecommandation />
        </TabPanel>
        <TabPanel currentTab={currentTab} index={2}>
          <AppRecommandation />
        </TabPanel>
      </Container>
      <Footer />
    </div>
  );
}

export default App;
