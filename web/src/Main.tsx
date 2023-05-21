import { useState } from "react";
import { makeStyles } from "@mui/styles";
import { AppBar, Box, Container, Divider, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Tab, Tabs, Toolbar } from "@mui/material";
import Header from './components/Header'
import Footer from './components/Footer'
import CarDetection from './pages/CarDetection'
import MusicRecommandation from './pages/MusicRecommandation'
import AppRecommandation from './pages/AppRecommandation'
import { theme } from './utils/Utils';
import MonteCarloEstimation from "./pages/MonteCarloEstimation";

const useStyles = makeStyles({
  main: {
    marginTop: 100,
    marginBottom: 100,
    "& > nav": {
      marginBottom: 50
    }
  },
  navBar: {
    maxHeight: 70,
  },
  menuBar: {
    [theme?.breakpoints.down('sm')]: {
      display: "none"
    },
    [theme?.breakpoints.down('sm')]: {
      display: "none"
    },
    '& .MuiDrawer-paper': {
      marginTop: 65,
      boxSizing: 'border-box',
      width: 240
    }
  }
});

interface SubsetTab{
  id: number,
  label: string
}

function App() {
  const classes = useStyles(theme);

  const [mobileOpen, setMobileOpen] = useState(false);
  const [selectedPage, setSelectedPage] = useState(0);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const pages = [{
      topic: "AI & ML",
      pages: [{
        name: "Car Detection",
        index: 0
      }],
    },{
      topic: "Reports",
      pages: [{
        name: "Music Recommendation",
        index: 1
      },{
        name: "Play Store App Recommendation",
        index: 2
      }]
    },{
      topic: "Maths",
      pages: [{
        name: "Monte Carlo Estimation",
        index: 3
      }]
    }
  ]

  const getCurrentPage = () => {
    switch(selectedPage){
      case 0:
        return <CarDetection />;
      case 1:
        return <MusicRecommandation />;
      case 2:
        return <AppRecommandation />;
      case 3:
        return <MonteCarloEstimation />;
    }
  }
  
  return (
    <div className="App">
      <Header />
      <AppBar position="fixed" className={classes.navBar}>
          <Toolbar>
            Application Collector
          </Toolbar>
        </AppBar>
        <Drawer variant="temporary" open={mobileOpen} onClose={handleDrawerToggle} className={classes.menuBar} ModalProps={{ keepMounted: true, }} >
          <Box>
            <List>
              {pages.map((topic, index) => (
                <Box key={topic.topic}>
                  <ListItem disablePadding>
                      <ListItemText primary={topic.topic} />
                  </ListItem>
                  {topic.pages.map((page, index) => (
                      <ListItem key={page.index} disablePadding>
                          <ListItemButton onClick={() => setSelectedPage(page.index)}>
                              <ListItemText primary={page.name} />
                          </ListItemButton> 
                      </ListItem>
                  ))}
              </Box>
              ))}
            </List>
          </Box>
        </Drawer>
        <Drawer variant="permanent" className={classes.menuBar} open>
          <Box>
            <List>
              {pages.map((topic, index) => (
                <Box key={topic.topic}>
                  <ListItem disablePadding>
                      <ListItemText primary={topic.topic} />
                  </ListItem>
                  {topic.pages.map((page, index) => (
                      <ListItem key={page.index} disablePadding>
                          <ListItemButton onClick={() => setSelectedPage(page.index)}>
                              <ListItemText primary={page.name} />
                          </ListItemButton> 
                      </ListItem>
                  ))}
              </Box>
              ))}
            </List>
          </Box>
        </Drawer>
      <Container maxWidth={"lg"} className={classes.main}>
        {getCurrentPage()}
      </Container>
      <Footer />
    </div>
  );
}

export default App;
