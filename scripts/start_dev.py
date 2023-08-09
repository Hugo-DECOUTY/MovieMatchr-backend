import uvicorn


def main():
    return uvicorn.run(
        "adminplatform:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="trace",
        debug=True,
    )


if __name__ == "__main__":
    main()
