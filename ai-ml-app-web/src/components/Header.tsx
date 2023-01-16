import { makeStyles } from "@mui/styles";
import { AppBar, Toolbar, Typography,  } from "@mui/material";

const useStyles = makeStyles({
    bar: {
        
    }
});

const Header = () => {
    const classes = useStyles();

    return (
        <AppBar component="nav" sx={{backgroundColor: "#f1f1f1", color: "black"}}>
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}>
                    AI & Machine Learning App
                </Typography>
            </Toolbar>
        </AppBar>
    )
}

export default Header;