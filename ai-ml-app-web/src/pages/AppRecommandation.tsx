import { makeStyles } from "@mui/styles";
import { Container} from "@mui/material";

const useStyles = makeStyles({
  main: {
    display: "flex !important",
    flexDirection: "column",
    alignItems: "center",
    gap: 15,
  },
});

const AppRecommandation = () => {
    const classes = useStyles();

    return (
        <Container className={classes.main} maxWidth={"md"}>
            <h2>Play Store App Recommandation</h2>
        </Container>
    )
}

export default AppRecommandation;