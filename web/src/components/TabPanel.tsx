import { useState } from "react";
import { makeStyles } from "@mui/styles";
import { Box, Typography } from "@mui/material";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    currentTab: number;
}

const useStyles = makeStyles({
    main: {
      display: "flex !important",
      marginTop: 100,
      flexDirection: "column",
      alignItems: "center",
      gap: 15,
      marginBottom: 100
    },
});

const TabPanel = (props: TabPanelProps) => {
    const { children, currentTab, index, ...other } = props;
    const classes = useStyles();

    return (
      <Box role="tabpanel" hidden={currentTab !== index} id={`simple-tabpanel-${index}`} aria-labelledby={`simple-tab-${index}`} {...other}>
        {currentTab === index && children}
      </Box>
    );
}

export default TabPanel;