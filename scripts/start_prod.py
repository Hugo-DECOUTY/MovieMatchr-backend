import uvicorn


def main():
    return uvicorn.run(
        "moviematchr:app",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
