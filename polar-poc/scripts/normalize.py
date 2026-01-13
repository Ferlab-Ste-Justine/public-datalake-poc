import argparse
import sys

from public_datalake.normalization import clinvar


def main():
    parser = argparse.ArgumentParser(description="Run normalization job")
    parser.add_argument("job", choices=["clinvar"], help="Normalization job name")
    args, remaining = parser.parse_known_args()

    # clinvar-specific argument parsing
    if args.job == "clinvar":
        job_parser = argparse.ArgumentParser(description="Clinvar normalization options")
        job_parser.add_argument("--input_path", required=True)
        job_parser.add_argument("--output_path", required=True)
        job_args = job_parser.parse_args(remaining)

        clinvar.run(input_path=job_args.input_path, output_path=job_args.output_path)
    
    else:
        print(f"Job '{args.job}' is not supported.")
        sys.exit(1) 


if __name__ == "__main__":
    main()