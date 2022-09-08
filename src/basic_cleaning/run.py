#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd



logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info(f"Downloaded input artifact to {artifact_local_path}")
    df_rental_nyc = pd.read_csv(artifact_local_path)


    ######################
    # YOUR CODE HERE     #
    ######################
    # Drop Outliers
    idx = df_rental_nyc['price'].between(args.min_price, args.max_price)
    df_rental_nyc = df_rental_nyc[idx].copy()
    # Covert last_review to datetime
    df_rental_nyc['last_review'] = pd.to_datetime(df_rental_nyc['last_review'])

    df_rental_nyc.to_csv(path_or_buf="clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help= "The artifact to download from W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help= "The artifact to upload to W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help= "The type of artifact to upload to W&B",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help= "The description of the artifact to upload to W&B",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help= "The minimum price to keep",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help= "The maximum price to keep",
        required=True
    )


    args = parser.parse_args()

    go(args)
