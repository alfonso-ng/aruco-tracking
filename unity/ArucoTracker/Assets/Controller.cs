using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPReceiver : MonoBehaviour
{
    [System.Serializable]
    public class PythonData
    {
        public VectorData position;
        public QuaternionData rotation;
    }

    [System.Serializable]
    public class VectorData
    {
        public float x;
        public float y;
        public float z;
    }

    [System.Serializable]
    public class QuaternionData
    {
        public float x;
        public float y;
        public float z;
        public float w;
    }

    Thread receiveThread;
    UdpClient client;
    public int port = 5005;

    // We use this to store the latest data safely
    private string lastReceivedPacket = "";
    private bool newDataAvailable = false;
    private readonly object lockObject = new object();

    void Start()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP); // This line "waits" for data

                string text = Encoding.UTF8.GetString(data);

                // Thread-safe update of the string
                lock (lockObject)
                {
                    lastReceivedPacket = text;
                    newDataAvailable = true;
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning(e.ToString());
            }
        }
    }

    void Update()
    {
        if (newDataAvailable)
        {
            string jsonToParse;
            lock (lockObject)
            {
                jsonToParse = lastReceivedPacket;
                newDataAvailable = false;
            }

            // Parse the nested JSON
            PythonData data = JsonUtility.FromJson<PythonData>(jsonToParse);

            // Apply Position
            transform.localPosition = new Vector3(
                data.position.x,
                data.position.y,
                data.position.z
            );

            // Apply Rotation
            transform.localRotation = new Quaternion(
                data.rotation.x,
                data.rotation.y,
                data.rotation.z,
                data.rotation.w
            );
        }
    }

    void OnQuit()
    {
        receiveThread.Abort();
        client.Close();
    }
}
