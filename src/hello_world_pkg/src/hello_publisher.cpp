#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "stdint.h"


class publisher_node : public rclcpp::Node
{
    public:
        publisher_node() : Node("Publisher")
    {
        publisher = this->create_publisher<std_msgs::msg::String>("Hello_World_Topic", 10);
        timer     = this->create_wall_timer(
                std::chrono::milliseconds(500),
                std::bind(&publisher_node::publisher_callback, this));

        RCLCPP_INFO(get_logger(), "Publisher Node Has Started");
    }

    private: 
        uint32_t counter = 0;
        void publisher_callback()
        {
            auto message = std_msgs::msg::String();

            message.data = "Hello World! ID: " + std::to_string(counter);

            RCLCPP_INFO(get_logger(), "Publishing the following: '%s'", message.data.c_str());
            publisher->publish(message);

            counter++;
        }

        // RCLCPP Config
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher;
        rclcpp::TimerBase                       ::SharedPtr timer;
};


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<publisher_node>();
    
    rclcpp::spin(node);
    rclcpp::shutdown();
}
