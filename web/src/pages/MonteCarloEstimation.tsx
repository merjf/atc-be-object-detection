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

const MonteCarloEstimation = () => {
    const classes = useStyles();

    return (
        <Container className={classes.main} maxWidth={"md"}>
            <h2>Monte Carlo Estimation</h2>
        </Container>
    )
}

export default MonteCarloEstimation;