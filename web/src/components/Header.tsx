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
                <Typography variant="h6" component="div">
                    Math, Statistical, AI & ML services
                </Typography>
            </Toolbar>
        </AppBar>
    )
}

export default Header;