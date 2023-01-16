import { makeStyles } from "@mui/styles";
import { AppBar, Box, Toolbar, Typography,  } from "@mui/material";

const useStyles = makeStyles({
    footer: {
        width: "-webkit-fill-available",
        display: "flex",
        position: "fixed",
        bottom: 0,
        alignItems: "center",
        height: "50px",
        borderTop: "1px solid grey",
        padding: "0px 5px",
        backgroundColor: "white"
    },
    signature: {
        width: "100%",
        paddingLeft: "5px",
    },
})

const Footer = () => {
    const classes = useStyles();

    return (
        <footer className={classes.footer}>
            <Box className={classes.signature}>
                <span>© 2023 - Francesco Mergiotti</span>
            </Box>
        </footer>
    )
}

export default Footer;