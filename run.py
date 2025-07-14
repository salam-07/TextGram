from echoapp import app

if __name__ == "__main__":
    # debug=True for reflecting changes to server on save
    app.run(host='0.0.0.0', port=5000, debug=True)