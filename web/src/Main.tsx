import { useState } from "react";
import { makeStyles } from "@mui/styles";
import { Box, Container, Tab, Tabs } from "@mui/material";
import Header from './components/Header'
import Footer from './components/Footer'
import CarDetection from './pages/CarDetection'
import MusicRecommandation from './pages/MusicRecommandation'
import AppRecommandation from './pages/AppRecommandation'
import MonteCarloEstimation from './pages/MonteCarloEstimation'
import { useEffect } from "react";
import TabPanel from "./components/TabPanel";

const useStyles = makeStyles({
  main: {
    marginTop: 100,
    marginBottom: 100,
    "& > nav": {
      marginBottom: 50
    }
  },
});

interface SubsetTab{
  id: number,
  label: string
}

function App() {
  const classes = useStyles();

  const [currentMainTab, setCurrentMainTab] = useState(0);
  const [currentSubsetTabs, setCurrentSubsetTabs] = useState<SubsetTab[]>([]);
  const [currentSubTab, setCurrentSubTab] = useState(10);

  const handleChangeMainTab = (event: React.SyntheticEvent, newTab: number) => {
    setCurrentMainTab(newTab);
  };

  const handleChangeSubTab = (event: React.SyntheticEvent, newTab: number) => {
    setCurrentSubTab((newTab+20));
  };

  const tabPanelProps = (index : number) => {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  useEffect(() => {
    switch(currentMainTab){
      case 0:
        setCurrentSubTab(10)
        setCurrentSubsetTabs([{
          id: 10,
          label: 'Monte Carlo Estimation'}]);
        break;
      case 1:
        setCurrentSubTab(20)
        setCurrentSubsetTabs([{
          id: 20,
          label: 'Car Detection'
        },{
          id: 21,
          label: 'Music Recommendation'
        },{
          id: 22,
          label: 'Play Store App Recommendation'
        }]);
        break;
      default:
        setCurrentMainTab(0)
        setCurrentSubTab(10)
        break;
    }
  }, [currentMainTab])
  
  return (
    <div className="App">
      <Header />
      <Container maxWidth={"lg"} className={classes.main}>
        <Box component="nav" sx={{ borderBottom: 1, borderColor: 'divider' }} >
          <Tabs value={currentMainTab} onChange={handleChangeMainTab} aria-label="Sections" centered>
            <Tab label="Math Apps" {...tabPanelProps(0)}/>
            <Tab label="AI & ML Apps" {...tabPanelProps(1)}/>
          </Tabs>
          <TabPanel currentTab={currentMainTab} index={0}>
            <Tabs value={currentSubTab} onChange={handleChangeSubTab} aria-label="Services" centered>
              {currentSubsetTabs.map( (subTab) => {
                return (
                  <Tab key={subTab.id} label={subTab.label} {...tabPanelProps(subTab.id)}/>
                )
              })}
            </Tabs>
          </TabPanel>
          <TabPanel currentTab={currentMainTab} index={1}>
            <Tabs value={currentSubTab} onChange={handleChangeSubTab} aria-label="Services" centered>
              {currentSubsetTabs.map( (subTab) => {
                return (
                  <Tab key={subTab.id} label={subTab.label} {...tabPanelProps(subTab.id)}/>
                )
              })}
            </Tabs>
          </TabPanel>
        </Box>
        <TabPanel currentTab={10} index={10}>
          <MonteCarloEstimation />
        </TabPanel>
        {/* <TabPanel currentTab={currentMainTab} index={0}>
          <TabPanel currentTab={currentSubTab} index={10}>
            <MonteCarloEstimation />
          </TabPanel>
        </TabPanel>
        <TabPanel currentTab={currentMainTab} index={1}>
          <TabPanel currentTab={currentSubTab} index={20}>
            <CarDetection />
          </TabPanel>
          <TabPanel currentTab={currentSubTab} index={21}>
            <MusicRecommandation />
          </TabPanel>
          <TabPanel currentTab={currentSubTab} index={22}>
            <AppRecommandation />
          </TabPanel>
        </TabPanel> */}
      </Container>
      <Footer />
    </div>
  );
}

export default App;
