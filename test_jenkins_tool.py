from jenkins_tool import get_last_build_status, trigger_jenkins_build

def test_build_status():
    status = get_last_build_status()
    print(f"Last build status: {status}")

def test_trigger_build():
    result = trigger_jenkins_build()
    print(result)

if __name__ == "__main__":
    test_build_status()
    test_trigger_build()
