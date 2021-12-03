using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class serverCall : MonoBehaviour
{
    string serverUrl = "http://localhost:8585";
    string sendConfigEndpoint = "/init";
    string agentUpdate = "/getCars";
    string updateEndpoint = "/update";
    string trafficLightUpdate = "/updateTrafficLights";
    AgentData carsData,obstacleData;
    semData semDataV;
    GameObject[] agents;

    bool hold = false;

    public GameObject carPrefab, fatherCar, semaforePrefabGreen, semaforePrefabRed, fatherSem;
    public float timeToUpdate = 5.0f, timer, dt; 
    
    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(SendInfo());
    }

    IEnumerator SendInfo()
    {
        WWWForm form = new WWWForm();
        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        yield return www.SendWebRequest();
        
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetSemaforeData());
        }
    }

    IEnumerator GetCarsData()
    {
        GameObject possible = GameObject.Find("fatherCars(Clone)");
        if(possible != null)
        {
            Destroy(possible);
        }

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + agentUpdate);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            Debug.Log("about to parse json for cars");
            obstacleData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            //GameObject[obstacleData.positions.Count];
            GameObject father = Instantiate(fatherCar, Vector3.zero, Quaternion.identity); 
            
            Debug.Log(obstacleData.positions.Count);
            for (int i = 0; i < obstacleData.positions.Count; i++)
            {
                
                GameObject box = Instantiate(carPrefab, obstacleData.positions[i], Quaternion.identity);
                box.transform.parent = GameObject.Find("fatherCars(Clone)").transform;
            }

            Debug.Log("json retrieved for car positions");
        }
    }

    IEnumerator GetSemaforeData()
    {
        GameObject possible = GameObject.Find("fatherSem(Clone)");
        if(possible != null)
        {
            Destroy(possible);
        }

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + trafficLightUpdate);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            Debug.Log("about to parse json for sems");
            Debug.Log(www.downloadHandler.text);
            semDataV = JsonUtility.FromJson<semData>(www.downloadHandler.text);

            //GameObject[obstacleData.positions.Count];
            GameObject father = Instantiate(fatherSem, Vector3.zero, Quaternion.identity); 
            
            for (int i = 0; i < semDataV.positions.Count; i++)
            {
                if (semDataV.state[i])
                {
                    GameObject box = Instantiate(semaforePrefabGreen, semDataV.positions[i], Quaternion.identity);
                    box.transform.parent = GameObject.Find("fatherSem(Clone)").transform;
                }
                else
                {
                    GameObject box = Instantiate(semaforePrefabRed, semDataV.positions[i], Quaternion.identity);
                    box.transform.parent = GameObject.Find("fatherSem(Clone)").transform;
                }
            }
            
            Debug.Log("json retrieved for sem positions");
            hold = false;
        }
    }

    // Update is called once per frame
    void Update()
    {
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold)
        {
            // Move time from the last frame
            timer += Time.deltaTime;
        } 
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetCarsData());
            StartCoroutine(GetSemaforeData());
        }
    }
}
